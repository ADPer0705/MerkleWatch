import typer
from pathlib import Path
from typing import Optional
from .filesystem import scan_directory
from .manifest import create_manifest_structure, save_manifest
from .verification import verify_directory, load_manifest, compare_manifests
from .diff import display_verification_diff, display_full_diff

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
        root_hash = scan_directory(directory, directory, manifest_data)
        
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

if __name__ == "__main__":
    app()
