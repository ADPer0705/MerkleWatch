import os
import typer
from pathlib import Path
from typing import Dict, Any, Optional
from .hashing import hash_file, compute_leaf_hash, compute_directory_hash
from .merkle import compute_merkle_root
from .ignore import IgnoreRules

def scan_directory(current_path: Path, root_path: Path, manifest_data: Dict[str, Any], ignore_rules: Optional[IgnoreRules] = None) -> str:
    """
    Recursively scan a directory, computing hashes and building the Merkle tree.
    
    Args:
        current_path: The directory currently being scanned.
        root_path: The root directory of the snapshot (for relative paths).
        manifest_data: Dictionary to collect file metadata and directory roots.
        ignore_rules: Optional IgnoreRules object to filter files.
        
    Returns:
        The Merkle root hash of the current directory.
        
    Raises:
        PermissionError: If directory cannot be accessed
        OSError: For other filesystem errors
    """
    
    # Get all children
    try:
        entries = sorted(os.listdir(current_path))
    except PermissionError as e:
        typer.echo(f"Warning: Permission denied accessing {current_path}", err=True)
        # Return empty hash for inaccessible directories
        # This allows the scan to continue but marks the directory as inaccessible
        return compute_merkle_root([])
    except OSError as e:
        typer.echo(f"Warning: Error accessing {current_path}: {e}", err=True)
        return compute_merkle_root([])

    child_hashes = []
    
    # We need to process children in sorted order to ensure deterministic tree
    for entry in entries:
        full_path = current_path / entry
        
        # Check ignore rules
        if ignore_rules and ignore_rules.should_ignore(full_path):
            continue
        
        # Skip symlinks to avoid loops and security issues
        # TODO: Implement symlink handling
        if full_path.is_symlink():
            typer.echo(f"Warning: Skipping symlink {full_path.relative_to(root_path)}", err=True)
            continue
            
        relative_path = full_path.relative_to(root_path).as_posix()
        
        try:
            if full_path.is_file():
                # 1. Hash file content
                try:
                    content_hash = hash_file(full_path)
                except (PermissionError, OSError) as e:
                    typer.echo(f"Warning: Cannot read file {relative_path}: {e}", err=True)
                    continue
                
                # 2. Wrap as leaf node
                leaf_hash = compute_leaf_hash(content_hash)
                child_hashes.append(leaf_hash)
                
                # 3. Store metadata
                stat = full_path.stat()
                manifest_data['files'][relative_path] = {
                    'size': stat.st_size,
                    'mtime': stat.st_mtime,
                    'content_hash': content_hash,
                    'leaf_hash': leaf_hash
                }
                
            elif full_path.is_dir():
                # 1. Recurse
                subdir_root = scan_directory(full_path, root_path, manifest_data, ignore_rules)
                
                # Skip empty or inaccessible directories (empty hash)
                if not subdir_root:
                    continue
                
                # 2. Wrap as directory node
                dir_node_hash = compute_directory_hash(subdir_root)
                child_hashes.append(dir_node_hash)
                
                # 3. Store directory metadata
                manifest_data['directories'][relative_path] = {
                    'root_hash': subdir_root,
                    'node_hash': dir_node_hash
                }
        except OSError as e:
            typer.echo(f"Warning: Error processing {relative_path}: {e}", err=True)
            continue
            
    # Compute Merkle root for this directory
    dir_merkle_root = compute_merkle_root(child_hashes)
    
    return dir_merkle_root
