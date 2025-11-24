"""
Ignore rules for MerkleWatch.
"""
import os
import fnmatch
from pathlib import Path
from typing import List, Set

class IgnoreRules:
    """Handle ignore patterns for file scanning."""
    
    def __init__(self, root_path: Path, ignore_file_name: str = ".merkleignore"):
        self.root_path = root_path
        self.patterns: List[str] = []
        self.ignore_file = root_path / ignore_file_name
        self.load_ignore_file()
        
    def load_ignore_file(self):
        """Load patterns from ignore file if it exists."""
        if self.ignore_file.exists():
            try:
                with open(self.ignore_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            self.patterns.append(line)
            except Exception:
                pass  # Fail silently on read errors
    
    def should_ignore(self, path: Path) -> bool:
        """
        Check if a path should be ignored based on patterns.
        
        Args:
            path: Path object to check (absolute or relative to root)
            
        Returns:
            True if path should be ignored
        """
        if not self.patterns:
            return False
            
        try:
            # Get path relative to root
            if path.is_absolute():
                rel_path = path.relative_to(self.root_path)
            else:
                rel_path = path
                
            # Convert to string with forward slashes for consistency
            path_str = str(rel_path).replace(os.sep, '/')
            
            # Also check if this is a directory for matching
            is_directory = path.is_dir()
            
            # Check each pattern
            for pattern in self.patterns:
                # Handle directory patterns (ending with /)
                if pattern.endswith('/'):
                    dir_pattern = pattern.rstrip('/')
                    
                    # Match exact directory name or files inside it
                    if path_str == dir_pattern:
                        return True
                    if path_str.startswith(dir_pattern + '/'):
                        return True
                        
                    # Match if any component of the path matches the pattern
                    parts = path_str.split('/')
                    if dir_pattern in parts:
                        return True
                        
                # Glob patterns with wildcards
                elif '*' in pattern or '?' in pattern or '[' in pattern:
                    # Standard glob matching
                    if fnmatch.fnmatch(path_str, pattern):
                        return True
                    # Also try matching just the basename
                    if fnmatch.fnmatch(os.path.basename(path_str), pattern):
                        return True
                        
                # Simple name patterns (no wildcards, no slashes)
                else:
                    # Check if this exact name appears in the path
                    parts = path_str.split('/')
                    if pattern in parts:
                        return True
                    # Also try exact path match
                    if path_str == pattern:
                        return True

            return False
            
        except ValueError:
            # Path is not relative to root
            return False
