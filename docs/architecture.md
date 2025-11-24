# Architecture

## Overview

MerkleWatch is designed as a modular, CLI-first application that creates cryptographically secure snapshots of directory structures using Merkle trees.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         CLI Layer                            │
│                    (cli.py - Typer)                          │
│  Commands: snapshot, verify, diff, ignore                    │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                      │
├──────────────────┬──────────────────┬───────────────────────┤
│  Verification    │   Comparison     │     Ignore Rules      │
│ (verification.py)│    (diff.py)     │     (ignore.py)       │
└──────────────────┴──────────────────┴───────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                   Core Algorithm Layer                       │
├──────────────────┬──────────────────┬───────────────────────┤
│   File System    │  Merkle Tree     │      Hashing          │
│ (filesystem.py)  │  (merkle.py)     │    (hashing.py)       │
└──────────────────┴──────────────────┴───────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                    Storage Layer                             │
│                  (manifest.py)                               │
│              JSON Manifest Files                             │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. CLI Layer (`cli.py`)

**Responsibility**: User interface and command handling

**Commands**:
- `snapshot`: Create a cryptographic snapshot
- `verify`: Verify directory against a manifest
- `diff`: Compare two manifests
- `ignore`: Configure ignore rules

**Technology**: Typer (modern Python CLI framework)

### 2. Hashing Module (`hashing.py`)

**Responsibility**: Low-level cryptographic operations

**Key Functions**:
- `hash_file()`: Hash file contents with chunked reading
- `compute_leaf_hash()`: Create file leaf nodes
- `compute_internal_hash()`: Combine two child nodes
- `compute_directory_hash()`: Create directory nodes

**Domain Separation**:
- `0x00`: File leaf nodes
- `0x01`: Internal tree nodes
- `0x02`: Directory nodes

**Security**: Prevents second-preimage attacks through domain separation

### 3. Merkle Tree Module (`merkle.py`)

**Responsibility**: Merkle tree construction

**Key Function**:
- `compute_merkle_root()`: Build balanced Merkle tree from leaf hashes

**Algorithm**:
1. Start with list of child hashes
2. Pair consecutive hashes
3. Hash each pair to create parent level
4. Repeat until single root hash remains
5. Handle odd numbers by duplicating last hash

### 4. Filesystem Module (`filesystem.py`)

**Responsibility**: Directory traversal and scanning

**Key Function**:
- `scan_directory()`: Recursive directory scanning

**Process**:
1. List and sort directory entries
2. Apply ignore rules
3. Hash files → create leaf nodes
4. Recurse into subdirectories → create directory nodes
5. Build Merkle tree from children
6. Store metadata in manifest structure

**Error Handling**:
- Permission errors: Warn and skip
- Symlinks: Skip to avoid loops
- OSErrors: Warn and continue
- Empty directories: Handle correctly

### 5. Manifest Module (`manifest.py`)

**Responsibility**: Manifest creation and storage

**Functions**:
- `create_manifest_structure()`: Assemble manifest data
- `save_manifest()`: Write JSON to file

**Manifest Structure**:
```json
{
  "merklewatch_version": "1.0.0",
  "algorithm": "sha256",
  "timestamp": 1732464642.123,
  "timestamp_iso": "2025-11-24T14:50:42Z",
  "root_hash": "...",
  "files": {...},
  "directories": {...}
}
```

### 6. Verification Module (`verification.py`)

**Responsibility**: Directory integrity verification

**Functions**:
- `load_manifest()`: Read manifest from JSON
- `compare_manifests()`: Find added/removed/modified files
- `verify_directory()`: Full verification workflow

**Verification Process**:
1. Load expected manifest
2. Scan current directory state
3. Compare root hashes
4. If mismatch, compute detailed diff
5. Return results with file-level details

### 7. Diff Module (`diff.py`)

**Responsibility**: Diff formatting and display

**Functions**:
- `display_added_files()`: Show added files (green)
- `display_removed_files()`: Show removed files (red)
- `display_modified_files_detailed()`: Show modified files with hashes (yellow)
- `display_full_diff()`: Complete diff view
- `display_verification_diff()`: Verification-specific output

**Output**: Color-coded, user-friendly diffs

### 8. Ignore Module (`ignore.py`)

**Responsibility**: Ignore rule handling

**Class**: `IgnoreRules`

**Methods**:
- `load_ignore_file()`: Read `.merkleignore`
- `should_ignore()`: Check if path matches ignore patterns

**Pattern Matching**:
- Directory patterns: `node_modules/`
- Glob patterns: `*.log`
- Simple names: `build`
- Comments and blank lines ignored

## Data Flow

### Snapshot Creation

```
User Command
    ↓
CLI: snapshot command
    ↓
Initialize IgnoreRules
    ↓
scan_directory (recursive)
    ├→ Check ignore rules
    ├→ Hash files → compute_leaf_hash
    ├→ Recurse subdirs → compute_directory_hash
    └→ compute_merkle_root
    ↓
create_manifest_structure
    ↓
save_manifest (JSON)
    ↓
Display root hash to user
```

### Verification

```
User Command
    ↓
CLI: verify command
    ↓
load_manifest (expected state)
    ↓
Initialize IgnoreRules
    ↓
scan_directory (current state)
    ↓
Compare root hashes
    ├→ Match: Success ✓
    └→ Mismatch:
        ↓
    compare_manifests
        ↓
    display_verification_diff
        ↓
    Exit with code 1
```

## Design Principles

### 1. Determinism

- **Sorted entries**: Filesystem entries always sorted alphabetically
- **Domain separation**: Consistent prefix bytes for node types
- **Platform independence**: POSIX path separators in manifests
- **Reproducible**: Same directory → same hash every time

### 2. Modularity

- **Clear separation**: Each module has single responsibility
- **Minimal coupling**: Modules interact through well-defined interfaces
- **Testability**: Pure functions where possible
- **Extensibility**: Easy to add new commands or features

### 3. Security

- **Cryptographic strength**: SHA-256 throughout
- **Domain separation**: Prevents collision attacks
- **No ambiguity**: File vs directory vs internal nodes always distinguished
- **Symlink handling**: Skip symlinks to prevent loops/attacks

### 4. Performance

- **Chunked reading**: 64KB chunks for large files
- **Streaming**: Files never fully loaded into memory
- **Efficient tree construction**: Balanced Merkle trees
- **Skip on errors**: Continue processing despite individual failures

### 5. Usability

- **Clear output**: Color-coded, structured messages
- **Helpful errors**: Warnings instead of crashes
- **Interactive mode**: Guided ignore configuration
- **Exit codes**: 0 for success, 1 for failure/changes

## File Format

### Manifest JSON

See [manifest-format.md](manifest-format.md) for detailed specification.

Key characteristics:
- **Human-readable**: JSON with indentation
- **Sorted keys**: Deterministic output
- **Complete metadata**: Size, mtime, hashes
- **Versioned**: Schema version tracking

### `.merkleignore`

- **Plain text**: One pattern per line
- **Comments**: Lines starting with `#`
- **Gitignore-like**: Familiar syntax
- **Optional**: No file = no ignores

## Security Considerations

### Threat Model

**Protected Against**:
- File content modification
- File addition/removal
- Directory structure changes
- Timestamp tampering
- File reordering

**Not Protected Against**:
- Manifest file modification (use external signing)
- Time-of-check-time-of-use races
- Physical access to system
- Compromised hashing implementation

### Recommendations

For production use:
1. Sign manifests with GPG or similar
2. Store manifests securely (offline, encrypted)
3. Use write-protected storage for archives
4. Implement access controls on manifest files
5. Combine with system audit logs

## Future Extensions

Potential areas for expansion:

1. **Parallel Hashing**: Multi-threaded file processing
2. **Progress Bars**: Visual feedback for large directories
3. **Compression**: Gzip manifests for large snapshots
4. **Incremental Snapshots**: Only hash changed files
5. **Merkle Proofs**: Verify individual files without full scan
6. **Remote Storage**: Cloud-based manifest storage
7. **Signing**: GPG integration for manifest signing
8. **Watch Mode**: Continuous monitoring
9. **Web UI**: Browser-based visualization

## Performance Characteristics

### Time Complexity

- **Hashing**: O(n) where n = total file size
- **Tree construction**: O(m log m) where m = number of files
- **Verification**: O(m) file comparisons

### Space Complexity

- **Memory**: O(m) for manifest structure
- **Disk**: O(m) for manifest file
- **No file caching**: Streaming keeps memory bounded

### Scalability

Tested with:
- ✅ Thousands of files
- ✅ Multi-gigabyte files
- ✅ Deep directory hierarchies
- ⚠️ Millions of files (may need optimization)

## Testing Strategy

### Unit Tests (Planned)

- Hash functions correctness
- Merkle tree construction
- Ignore rule matching
- Manifest serialization

### Integration Tests (Planned)

- Full snapshot workflows
- Verification with changes
- Diff comparison
- Error handling scenarios

### Edge Cases

- Empty directories
- Single file
- Permission errors
- Symlinks
- Unicode filenames
- Large files (>1GB)

## Dependencies

### Runtime

- **Python**: 3.10+
- **typer**: CLI framework
- **questionary**: Interactive prompts

### Development

- **pytest**: Testing framework
- **ruff**: Linting
- **black**: Code formatting

## Version History

See [CHANGELOG.md](../CHANGELOG.md) for detailed version history.
