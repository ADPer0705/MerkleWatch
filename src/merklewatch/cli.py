import typer
import questionary
import os
from pathlib import Path
from .filesystem import scan_directory
from .manifest import create_manifest_structure, save_manifest
from .verification import verify_directory, load_manifest, compare_manifests
from .diff import display_verification_diff, display_full_diff
from .ignore import IgnoreRules
from .common_ignores import COMMON_IGNORES, get_all_common_patterns
import fnmatch

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

        # If the output manifest is inside the scanned directory, temporarily ignore it
        try:
            rel_out = out.relative_to(directory)
            # ignore the relative path and the filename
            ignore_rules.add_pattern(str(rel_out))
            ignore_rules.add_pattern(rel_out.name)
        except Exception:
            # output is not inside directory — nothing to do
            pass
        
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
    Interactively configure .merkleignore rules.
    """
    typer.echo(f"Scanning {directory} for ignore suggestions...")
    
    ignore_rules = IgnoreRules(directory)
    existing_patterns = set(ignore_rules.patterns)
    
    # Collect all relative paths for fuzzy finding and pattern matching
    all_paths = []
    try:
        for root, dirs, files in os.walk(directory):
            # Skip .git and other common hidden dirs to speed up and avoid noise
            if '.git' in dirs:
                dirs.remove('.git')
                
            rel_root = Path(root).relative_to(directory)
            
            if rel_root != Path('.'):
                all_paths.append(str(rel_root) + '/')
            
            for f in files:
                path = rel_root / f
                all_paths.append(str(path))
    except Exception as e:
        typer.echo(f"Error scanning directory: {e}", err=True)
        raise typer.Exit(code=1)

    # Find relevant common patterns
    suggested_patterns = []
    common_patterns = get_all_common_patterns()
    
    # Check which common patterns match files in the directory
    # This is a simple check: does this pattern match ANY file we found?
    matched_common = set()
    
    with typer.progressbar(common_patterns, label="Checking common patterns") as progress:
        for pattern in progress:
            # Check if pattern matches any path
            # We need to handle directory patterns (ending in /) vs file patterns
            is_match = False
            for path in all_paths:
                if pattern.endswith('/'):
                    if path.startswith(pattern) or fnmatch.fnmatch(path, pattern):
                        is_match = True
                        break
                else:
                    if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
                        is_match = True
                        break
            
            if is_match:
                matched_common.add(pattern)

    # Group matched patterns by category for display
    choices = []
    for category, patterns in COMMON_IGNORES.items():
        category_matches = [p for p in patterns if p in matched_common]
        if category_matches:
            choices.append(questionary.Separator(f"--- {category} ---"))
            for p in category_matches:
                checked = p in existing_patterns
                choices.append(questionary.Choice(p, checked=checked))

    if choices:
        typer.echo("\nFound common patterns matching files in your directory:")
        selected = questionary.checkbox(
            "Select patterns to ignore:",
            choices=choices
        ).ask()
        
        if selected is not None:
            # Add selected, remove unselected (only from the set of common patterns we presented)
            # Actually, safer to just add selected ones that aren't there, 
            # and maybe ask about removing ones that were there but unchecked?
            # For simplicity, let's just ensure selected are in.
            for p in selected:
                ignore_rules.add_pattern(p)
    else:
        typer.echo("No common ignore patterns matched files in this directory.")

    # Main interaction loop
    while True:
        action = questionary.select(
            "What would you like to do?",
            choices=[
                "Add file/directory (Fuzzy Find)",
                "Add pattern (Manual)",
                "Remove pattern",
                "View current patterns",
                "Save & Exit",
                "Cancel"
            ]
        ).ask()
        
        if action == "Add file/directory (Fuzzy Find)":
            target = questionary.autocomplete(
                "Start typing to find file/directory:",
                choices=all_paths
            ).ask()
            if target:
                ignore_rules.add_pattern(target)
                typer.echo(f"Added: {target}")
                
        elif action == "Add pattern (Manual)":
            pattern = questionary.text("Enter ignore pattern:").ask()
            if pattern:
                ignore_rules.add_pattern(pattern)
                typer.echo(f"Added: {pattern}")
                
        elif action == "Remove pattern":
            if not ignore_rules.patterns:
                typer.echo("No patterns to remove.")
                continue
                
            to_remove = questionary.checkbox(
                "Select patterns to remove:",
                choices=[questionary.Choice(p) for p in ignore_rules.patterns]
            ).ask()
            
            if to_remove:
                for p in to_remove:
                    ignore_rules.remove_pattern(p)
                typer.echo(f"Removed {len(to_remove)} patterns.")
                
        elif action == "View current patterns":
            typer.echo("\nCurrent Ignore Patterns:")
            for p in ignore_rules.patterns:
                typer.echo(f"  - {p}")
            typer.echo("")
            
        elif action == "Save & Exit":
            if ignore_rules.save():
                typer.echo(f"Saved ignore rules to {ignore_rules.ignore_file}")
            break
            
        elif action == "Cancel":
            typer.echo("Changes discarded.")
            break

if __name__ == "__main__":
    app()
