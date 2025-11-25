import typer
import questionary
import os
from pathlib import Path
from .filesystem import scan_directory
from .manifest import create_manifest_structure, save_manifest
from .verification import verify_directory, load_manifest, compare_manifests
from .diff import display_verification_diff, display_full_diff
from .ignore import IgnoreRules

app = typer.Typer()

@app.command()
def snapshot(
    directory: Path = typer.Argument(..., help="The directory to snapshot", exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    out: Path = typer.Option(..., "--out", "-o", help="Output path for the manifest JSON file")
):
    """
    Create a Merkle tree snapshot of a directory.
    """
    typer.echo(f"Snapshoting {directory}...")
    
    manifest_data = {'files': {}, 'directories': {}}
    
    try:
        # Initialize ignore rules
        ignore_rules = IgnoreRules(directory)
        
        root_hash = scan_directory(directory, directory, manifest_data, ignore_rules)
        
        manifest = create_manifest_structure(root_hash, manifest_data)
        
        save_manifest(manifest, out)
        
        typer.echo(f"Snapshot created successfully!")
        typer.echo(f"Root Hash: {root_hash}")
        typer.echo(f"Manifest saved to: {out}")
        
    except Exception as e:
        typer.echo(f"Error creating snapshot: {e}", err=True)
        raise typer.Exit(code=1)

@app.command()
def verify(
    manifest_path: Path = typer.Argument(..., help="Path to the manifest file", exists=True, dir_okay=False, resolve_path=True),
    directory: Path = typer.Argument(..., help="The directory to verify", exists=True, file_okay=False, dir_okay=True, resolve_path=True)
):
    """
    Verify a directory against a manifest.
    """
    typer.echo(f"Verifying {directory} against {manifest_path}...")
    
    try:
        success, expected, actual, diffs, old_files, new_files = verify_directory(manifest_path, directory)
        
        if success:
            typer.echo(typer.style("\n✓ Verification SUCCESSFUL!", fg=typer.colors.GREEN, bold=True))
            typer.echo(f"Root Hash matches: {actual}")
        else:
            display_verification_diff(expected, actual, diffs, old_files, new_files)
            raise typer.Exit(code=1)
            
    except Exception as e:
        typer.echo(f"Error during verification: {e}", err=True)
        raise typer.Exit(code=1)

@app.command()
def diff(
    manifest1: Path = typer.Argument(..., help="Path to the first (old) manifest file", exists=True, dir_okay=False, resolve_path=True),
    manifest2: Path = typer.Argument(..., help="Path to the second (new) manifest file", exists=True, dir_okay=False, resolve_path=True)
):
    """
    Compare two manifest files to see what changed between snapshots.
    """
    typer.echo(f"Comparing {manifest1} → {manifest2}...\n")
    
    try:
        # Load both manifests
        old_manifest = load_manifest(manifest1)
        new_manifest = load_manifest(manifest2)
        
        # Display manifest metadata
        typer.echo(f"Old manifest: {old_manifest.get('timestamp_iso', 'N/A')}")
        typer.echo(f"  Root Hash: {old_manifest.get('root_hash', 'N/A')}")
        typer.echo(f"\nNew manifest: {new_manifest.get('timestamp_iso', 'N/A')}")
        typer.echo(f"  Root Hash: {new_manifest.get('root_hash', 'N/A')}")
        
        # Compare manifests
        diffs = compare_manifests(old_manifest, new_manifest)
        
        # Display diff
        display_full_diff(
            diffs, 
            old_manifest.get('files', {}), 
            new_manifest.get('files', {}),
            show_detailed=True
        )
        
        # Exit with code 1 if there are differences (similar to diff command convention)
        total_changes = len(diffs.get('added', [])) + len(diffs.get('removed', [])) + len(diffs.get('modified', []))
        if total_changes > 0:
            raise typer.Exit(code=1)
            
    except Exception as e:
        typer.echo(f"Error comparing manifests: {e}", err=True)
        raise typer.Exit(code=1)

@app.command()
def ignore(
    directory: Path = typer.Argument(..., help="The directory to configure ignores for", exists=True, file_okay=False, dir_okay=True, resolve_path=True)
):
    """
    Interactively configure .merkleignore file.
    """
    ignore_file = directory / ".merkleignore"
    
    # 1. Load existing ignores
    existing_ignores = []
    if ignore_file.exists():
        with open(ignore_file, 'r') as f:
            existing_ignores = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    typer.echo(f"Configuring ignores for {directory}")
    if existing_ignores:
        typer.echo(f"Found {len(existing_ignores)} existing ignore patterns.")
    
    # 2. Scan for common junk
    common_patterns = [
        ".git/", "__pycache__/", "node_modules/", ".DS_Store", 
        "venv/", ".env", "dist/", "build/", "*.pyc", ".pytest_cache/"
    ]
    
    found_common = []
    # Simple check if these exist in root
    for pattern in common_patterns:
        clean_pattern = pattern.rstrip('/')
        if (directory / clean_pattern).exists() or any(directory.glob(pattern)):
            if pattern not in existing_ignores:
                found_common.append(pattern)
    
    new_ignores = []
    
    # 3. Ask to add common ignores
    if found_common:
        selected_common = questionary.checkbox(
            "Found common ignore candidates. Select ones to add:",
            choices=[questionary.Choice(p, checked=True) for p in found_common]
        ).ask()
        
        if selected_common:
            new_ignores.extend(selected_common)
            
    # 4. Interactive file picker
    if questionary.confirm("Do you want to browse and ignore other files/directories?").ask():
        # Get all files and directories (limit depth to avoid massive lists?)
        # For now, let's just do top-level and maybe one level deep or just top level?
        # A full recursive tree might be too big for a simple list.
        # Let's do a recursive scan but limit to reasonable count or depth.
        
        paths = []
        for root, dirs, files in os.walk(directory):
            # Skip .git and other hidden dirs to avoid noise
            if '.git' in dirs:
                dirs.remove('.git')
                
            rel_root = Path(root).relative_to(directory)
            
            if rel_root == Path('.'):
                prefix = ""
            else:
                prefix = str(rel_root) + "/"
                
            for d in dirs:
                path = prefix + d + "/"
                if path not in existing_ignores and path not in new_ignores:
                    paths.append(path)
            
            for f in files:
                path = prefix + f
                if path not in existing_ignores and path not in new_ignores and path != ".merkleignore":
                    paths.append(path)
                    
        # Sort paths
        paths.sort()
        
        if paths:
            selected_custom = questionary.checkbox(
                "Select files/directories to ignore (use space to select, type to filter):",
                choices=paths
            ).ask()
            
            if selected_custom:
                new_ignores.extend(selected_custom)
        else:
            typer.echo("No other files found to ignore.")

    # 5. Save
    if new_ignores:
        all_ignores = existing_ignores + new_ignores
        # Remove duplicates while preserving order
        unique_ignores = list(dict.fromkeys(all_ignores))
        
        with open(ignore_file, 'w') as f:
            for pattern in unique_ignores:
                f.write(f"{pattern}\n")
                
        typer.echo(f"Updated {ignore_file} with {len(new_ignores)} new patterns.")
    else:
        typer.echo("No changes made.")

if __name__ == "__main__":
    app()
