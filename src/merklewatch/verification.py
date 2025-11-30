import json
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from .filesystem import scan_directory
from .ignore import IgnoreRules

def load_manifest(manifest_path: Path) -> Dict[str, Any]:
    with open(manifest_path, 'r') as f:
        return json.load(f)

def compare_manifests(old_manifest: Dict[str, Any], new_manifest_data: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Compare two manifest data structures to find added, removed, and modified files.
    """
    old_files = old_manifest.get('files', {})
    new_files = new_manifest_data.get('files', {})
    
    added = []
    removed = []
    modified = []
    
    old_paths = set(old_files.keys())
    new_paths = set(new_files.keys())
    
    # Added files
    for path in new_paths - old_paths:
        added.append(path)
        
    # Removed files
    for path in old_paths - new_paths:
        removed.append(path)
        
    # Modified files
    for path in old_paths & new_paths:
        if old_files[path]['content_hash'] != new_files[path]['content_hash']:
            modified.append(path)
            
    return {
        'added': sorted(added),
        'removed': sorted(removed),
        'modified': sorted(modified)
    }

def verify_directory(manifest_path: Path, target_directory: Path) -> Tuple[bool, Optional[str], str, Dict[str, List[str]], Dict[str, Any], Dict[str, Any]]:
    """
    Verify a directory against a manifest.
    
    Returns:
        Tuple containing:
        - success (bool): True if verification passed (hashes match)
        - expected_root (str): The root hash from the manifest
        - actual_root (str): The computed root hash
        - diffs (dict): Dictionary of added, removed, modified files
        - old_files (dict): Original manifest file data
        - new_files (dict): Current directory file data
    """
    # 1. Load Manifest
    manifest = load_manifest(manifest_path)
    expected_root = manifest.get('root_hash')
    
    # 2. Scan Directory
    # Initialize ignore rules
    ignore_rules = IgnoreRules(target_directory)
    
    new_manifest_data = {'files': {}, 'directories': {}}
    actual_root = scan_directory(target_directory, target_directory, new_manifest_data, ignore_rules)
    
    # 3. Compare
    success = (expected_root == actual_root)
    
    diffs = {}
    if not success:
        diffs = compare_manifests(manifest, new_manifest_data)
        
    return success, expected_root, actual_root, diffs, manifest.get('files', {}), new_manifest_data.get('files', {})
