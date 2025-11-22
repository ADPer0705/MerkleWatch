from typing import List
from .hashing import compute_internal_hash

def compute_merkle_root(hashes: List[str]) -> str:
    """
    Compute the Merkle root for a list of hashes.
    The hashes should already be sorted (e.g., by filename) before calling this.
    """
    if not hashes:
        # Return a hash of empty bytes or a specific constant for empty directory?
        # For now, let's return a hash of empty string with internal prefix, 
        # or maybe just a null hash. 
        # Let's assume an empty directory has a specific hash.
        # But wait, SHA256(0x01 || empty || empty)?
        # Let's stick to a simple convention: if empty, maybe return a hash of empty bytes?
        # Or maybe the caller ensures it's never empty?
        # A directory can be empty.
        # Let's use a placeholder for now, or just hash of empty bytes.
        # README doesn't specify empty directory behavior.
        # I'll return a hash of an empty string for now to be safe.
        # Actually, standard Merkle trees usually handle empty lists by returning a specific zero hash.
        # Let's return the hash of an empty string using the internal prefix for consistency?
        # Or just return None?
        # Let's return a hash of empty bytes with LEAF prefix? No, it's a directory.
        # Let's just return a hash of b''.
        from .hashing import hash_node, PREFIX_INTERNAL
        return hash_node(PREFIX_INTERNAL, b'')

    current_level = hashes

    while len(current_level) > 1:
        next_level = []
        
        # If odd, duplicate last
        if len(current_level) % 2 != 0:
            current_level.append(current_level[-1])
        
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i+1]
            parent = compute_internal_hash(left, right)
            next_level.append(parent)
        
        current_level = next_level

    return current_level[0]
