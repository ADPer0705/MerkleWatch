"""
MerkleWatch - Deterministic integrity verification using Merkle trees
"""

__version__ = "0.1.0"
__author__ = "ADPer"
__email__ = "adper0705@gmail.com"

from .hashing import (
    hash_file,
    compute_leaf_hash,
    compute_internal_hash,
    compute_directory_hash,
)
from .merkle import compute_merkle_root
from .filesystem import scan_directory
from .manifest import create_manifest_structure, save_manifest

__all__ = [
    "hash_file",
    "compute_leaf_hash",
    "compute_internal_hash",
    "compute_directory_hash",
    "compute_merkle_root",
    "scan_directory",
    "create_manifest_structure",
    "save_manifest",
]
