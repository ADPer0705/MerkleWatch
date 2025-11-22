import os
from pathlib import Path
from typing import Dict, List, Tuple, Any
from .hashing import hash_file, compute_leaf_hash, compute_directory_hash
from .merkle import compute_merkle_root

def scan_directory(current_path: Path, root_path: Path, manifest_data: Dict[str, Any]) -> str:
    """
    Recursively scan a directory, computing hashes and building the Merkle tree.
    
    Args:
        current_path: The directory currently being scanned.
        root_path: The root directory of the snapshot (for relative paths).
        manifest_data: Dictionary to collect file metadata and directory roots.
        
    Returns:
        The Merkle root hash of the current directory.
    """
    
    # Get all children
    try:
        entries = sorted(os.listdir(current_path))
    except PermissionError:
        # Handle permission errors gracefully? For now, maybe skip or error.
        # Let's print a warning and return a placeholder? 
        # Or just let it crash for v0.1.0
        print(f"Warning: Permission denied accessing {current_path}")
        return "" # Should probably handle this better in a real tool

    child_hashes = []
    
    # We need to process children in sorted order to ensure deterministic tree
    for entry in entries:
        full_path = current_path / entry
        relative_path = full_path.relative_to(root_path).as_posix()
        
        if full_path.is_file():
            # 1. Hash file content
            content_hash = hash_file(full_path)
            
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
            subdir_root = scan_directory(full_path, root_path, manifest_data)
            
            # 2. Wrap as directory node
            dir_node_hash = compute_directory_hash(subdir_root)
            child_hashes.append(dir_node_hash)
            
            # 3. Store directory metadata
            manifest_data['directories'][relative_path] = {
                'root_hash': subdir_root,
                'node_hash': dir_node_hash
            }
            
    # Compute Merkle root for this directory
    dir_merkle_root = compute_merkle_root(child_hashes)
    
    return dir_merkle_root
