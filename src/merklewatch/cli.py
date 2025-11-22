import typer
from pathlib import Path
from typing import Optional
from .filesystem import scan_directory
from .manifest import create_manifest_structure, save_manifest
from .verification import verify_directory

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
        success, expected, actual, diffs = verify_directory(manifest_path, directory)
        
        if success:
            typer.echo(typer.style("Verification SUCCESSFUL!", fg=typer.colors.GREEN, bold=True))
            typer.echo(f"Root Hash matches: {actual}")
        else:
            typer.echo(typer.style("Verification FAILED!", fg=typer.colors.RED, bold=True))
            typer.echo(f"Expected Root: {expected}")
            typer.echo(f"Actual Root:   {actual}")
            
            if diffs['modified']:
                typer.echo("\nModified files:")
                for f in diffs['modified']:
                    typer.echo(f"  - {f}")
                    
            if diffs['removed']:
                typer.echo("\nMissing files (removed):")
                for f in diffs['removed']:
                    typer.echo(f"  - {f}")
                    
            if diffs['added']:
                typer.echo("\nNew files (added):")
                for f in diffs['added']:
                    typer.echo(f"  - {f}")
            
            raise typer.Exit(code=1)
            
    except Exception as e:
        typer.echo(f"Error during verification: {e}", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
