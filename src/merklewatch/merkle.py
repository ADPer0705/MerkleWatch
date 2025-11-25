from typing import List
from .hashing import compute_internal_hash

def compute_merkle_root(hashes: List[str]) -> str:
    """
    Compute the Merkle root for a list of hashes.
    The hashes should already be sorted (e.g., by filename) before calling this.
    """
    if not hashes:
        # Empty tree case
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
