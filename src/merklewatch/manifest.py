import json
import time
from pathlib import Path
from typing import Dict, Any

def create_manifest_structure(root_hash: str, manifest_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Assemble the final manifest dictionary.
    """
    return {
        "merklewatch_version": "0.1.0",
        "algorithm": "sha256",
        "timestamp": time.time(),
        "timestamp_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "root_hash": root_hash,
        "files": manifest_data.get('files', {}),
        "directories": manifest_data.get('directories', {})
    }

def save_manifest(manifest: Dict[str, Any], output_path: Path):
    """
    Save the manifest to a JSON file.
    """
    with open(output_path, 'w') as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
