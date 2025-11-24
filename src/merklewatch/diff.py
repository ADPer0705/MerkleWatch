"""
Diff formatting and display utilities for MerkleWatch.
"""
import typer
from typing import Dict, List, Any, Optional


def format_diff_summary(diffs: Dict[str, List[str]]) -> str:
    """
    Format a summary of the differences.
    
    Args:
        diffs: Dictionary with 'added', 'removed', 'modified' keys
        
    Returns:
        Formatted summary string
    """
    total = len(diffs.get('added', [])) + len(diffs.get('removed', [])) + len(diffs.get('modified', []))
    
    parts = []
    if diffs.get('added'):
        parts.append(f"{len(diffs['added'])} added")
    if diffs.get('removed'):
        parts.append(f"{len(diffs['removed'])} removed")
    if diffs.get('modified'):
        parts.append(f"{len(diffs['modified'])} modified")
        
    return f"{total} changes: {', '.join(parts)}"


def display_added_files(files: List[str], show_header: bool = True):
    """Display added files in green."""
    if not files:
        return
        
    if show_header:
        typer.echo(typer.style("\n✓ Added files:", fg=typer.colors.GREEN, bold=True))
    
    for file in files:
        typer.echo(typer.style(f"  + {file}", fg=typer.colors.GREEN))


def display_removed_files(files: List[str], show_header: bool = True):
    """Display removed files in red."""
    if not files:
        return
        
    if show_header:
        typer.echo(typer.style("\n✗ Removed files:", fg=typer.colors.RED, bold=True))
    
    for file in files:
        typer.echo(typer.style(f"  - {file}", fg=typer.colors.RED))


def display_modified_files(files: List[str], show_header: bool = True):
    """Display modified files in yellow."""
    if not files:
        return
        
    if show_header:
        typer.echo(typer.style("\n⚠ Modified files:", fg=typer.colors.YELLOW, bold=True))
    
    for file in files:
        typer.echo(typer.style(f"  M {file}", fg=typer.colors.YELLOW))


def display_modified_files_detailed(
    files: List[str], 
    old_data: Dict[str, Any], 
    new_data: Dict[str, Any],
    show_header: bool = True
):
    """
    Display modified files with old and new hash information.
    
    Args:
        files: List of modified file paths
        old_data: Old manifest file data (manifest['files'])
        new_data: New manifest file data
        show_header: Whether to show the section header
    """
    if not files:
        return
        
    if show_header:
        typer.echo(typer.style("\n⚠ Modified files:", fg=typer.colors.YELLOW, bold=True))
    
    for file in files:
        typer.echo(typer.style(f"  M {file}", fg=typer.colors.YELLOW))
        
        old_hash = old_data.get(file, {}).get('content_hash', 'N/A')
        new_hash = new_data.get(file, {}).get('content_hash', 'N/A')
        
        typer.echo(f"      Old: {typer.style(old_hash, fg=typer.colors.RED, dim=True)}")
        typer.echo(f"      New: {typer.style(new_hash, fg=typer.colors.GREEN, dim=True)}")


def display_full_diff(
    diffs: Dict[str, List[str]], 
    old_data: Optional[Dict[str, Any]] = None,
    new_data: Optional[Dict[str, Any]] = None,
    show_detailed: bool = True
):
    """
    Display a complete diff with all changes.
    
    Args:
        diffs: Dictionary with 'added', 'removed', 'modified' keys
        old_data: Optional old manifest file data for detailed view
        new_data: Optional new manifest file data for detailed view
        show_detailed: Whether to show hash details for modified files
    """
    total = len(diffs.get('added', [])) + len(diffs.get('removed', [])) + len(diffs.get('modified', []))
    
    if total == 0:
        typer.echo(typer.style("No differences found.", fg=typer.colors.GREEN))
        return
    
    typer.echo(f"\n{typer.style('Summary:', bold=True)} {format_diff_summary(diffs)}")
    
    # Display each category
    display_added_files(diffs.get('added', []))
    display_removed_files(diffs.get('removed', []))
    
    if show_detailed and old_data and new_data and diffs.get('modified'):
        display_modified_files_detailed(diffs['modified'], old_data, new_data)
    else:
        display_modified_files(diffs.get('modified', []))


def display_verification_diff(
    expected_root: str,
    actual_root: str,
    diffs: Dict[str, List[str]],
    old_data: Optional[Dict[str, Any]] = None,
    new_data: Optional[Dict[str, Any]] = None
):
    """
    Display verification failure with detailed diff information.
    
    Args:
        expected_root: Expected root hash from manifest
        actual_root: Actual computed root hash
        diffs: Dictionary with 'added', 'removed', 'modified' keys
        old_data: Original manifest file data
        new_data: Current directory file data
    """
    typer.echo(typer.style("\n✗ Verification FAILED!", fg=typer.colors.RED, bold=True))
    typer.echo(f"\nRoot Hash Mismatch:")
    typer.echo(f"  Expected: {typer.style(expected_root, fg=typer.colors.RED, dim=True)}")
    typer.echo(f"  Actual:   {typer.style(actual_root, fg=typer.colors.GREEN, dim=True)}")
    
    display_full_diff(diffs, old_data, new_data, show_detailed=True)
