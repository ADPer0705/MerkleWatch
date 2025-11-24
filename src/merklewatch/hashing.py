import hashlib
from pathlib import Path
from typing import Union

# Domain separation prefixes
PREFIX_LEAF = b'\x00'
PREFIX_INTERNAL = b'\x01'
PREFIX_DIR = b'\x02'

def sha256_bytes(data: bytes) -> bytes:
    """Compute SHA256 hash of bytes."""
    return hashlib.sha256(data).digest()

def hash_node(prefix: bytes, data: bytes) -> str:
    """
    Hash a node with a domain separation prefix.
    Returns the hex string of the hash.
    """
    return hashlib.sha256(prefix + data).hexdigest()

def hash_file(filepath: Path) -> str:
    """
    Compute the hash of a file's content using chunked reading.
    Returns the raw SHA256 hash (hex) of the content.
    Note: This is the raw content hash. The leaf node hash will wrap this.
    
    Raises:
        PermissionError: If file cannot be read due to permissions
        OSError: If file cannot be read for other reasons
    """
    hasher = hashlib.sha256()
    buffer_size = 65536  # 64kb chunks

    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(buffer_size):
                hasher.update(chunk)
    except PermissionError:
        raise PermissionError(f"Permission denied reading file: {filepath}")
    except OSError as e:
        raise OSError(f"Error reading file {filepath}: {e}")
    
    return hasher.hexdigest()

def compute_leaf_hash(file_hash_hex: str) -> str:
    """
    Compute the leaf node hash from a file's content hash.
    leaf_hash = SHA256(0x00 || file_hash_bytes)
    """
    # Convert hex string back to bytes for the inner hash
    file_hash_bytes = bytes.fromhex(file_hash_hex)
    return hash_node(PREFIX_LEAF, file_hash_bytes)

def compute_internal_hash(left_hex: str, right_hex: str) -> str:
    """
    Compute hash for an internal Merkle node.
    internal_hash = SHA256(0x01 || left_bytes || right_bytes)
    """
    left_bytes = bytes.fromhex(left_hex)
    right_bytes = bytes.fromhex(right_hex)
    return hash_node(PREFIX_INTERNAL, left_bytes + right_bytes)

def compute_directory_hash(subdir_root_hex: str) -> str:
    """
    Compute hash for a directory node (which represents a subdirectory).
    dir_node = SHA256(0x02 || subdirectory_root_hash_bytes)
    """
    root_bytes = bytes.fromhex(subdir_root_hex)
    return hash_node(PREFIX_DIR, root_bytes)
