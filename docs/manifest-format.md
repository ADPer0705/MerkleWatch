# Manifest Format Specification

## Overview

MerkleWatch manifests are JSON files that capture the complete state of a directory structure at a specific point in time. They include cryptographic hashes, metadata, and structural information.

## File Extension

Recommended: `.json`

Example: `snapshot_2025-11-24.json`

## Format Version

Current version: `1.0.0`

## Root Schema

```json
{
  "merklewatch_version": "1.0.0",
  "algorithm": "sha256",
  "timestamp": 1732464642.123456,
  "timestamp_iso": "2025-11-24T14:50:42Z",
  "root_hash": "a7304db0e614521b6cd9c79bfaa8707f845c5f9f509bbc8286f040461b0820b9",
  "files": { ... },
  "directories": { ... }
}
```

## Field Descriptions

### Top-Level Fields

#### `merklewatch_version` (string, required)

The version of MerkleWatch that created this manifest.

- **Format**: Semantic versioning (`MAJOR.MINOR.PATCH`)
- **Example**: `"1.0.0"`
- **Purpose**: Schema compatibility checking

#### `algorithm` (string, required)

The cryptographic hash algorithm used.

- **Value**: `"sha256"`
- **Purpose**: Future-proofing for algorithm changes

#### `timestamp` (number, required)

Unix timestamp when the snapshot was created.

- **Format**: Seconds since epoch (with fractional seconds)
- **Example**: `1732464642.123456`
- **Precision**: Microseconds
- **Purpose**: Temporal ordering of snapshots

#### `timestamp_iso` (string, required)

Human-readable ISO 8601 timestamp (UTC).

- **Format**: `YYYY-MM-DDTHH:MM:SSZ`
- **Example**: `"2025-11-24T14:50:42Z"`
- **Purpose**: Human readability

#### `root_hash` (string, required)

The Merkle root hash of the entire directory structure.

- **Format**: 64-character hexadecimal string (SHA-256)
- **Example**: `"a7304db0e614521b6cd9c79bfaa8707f845c5f9f509bbc8286f040461b0820b9"`
- **Purpose**: Single hash representing complete directory state

#### `files` (object, required)

Dictionary mapping relative file paths to file metadata.

- **Keys**: Relative file paths (POSIX-style with `/` separator)
- **Values**: File metadata objects
- **Empty**: `{}` if no files

#### `directories` (object, required)

Dictionary mapping relative directory paths to directory metadata.

- **Keys**: Relative directory paths (POSIX-style with `/` separator)
- **Values**: Directory metadata objects
- **Empty**: `{}` if no subdirectories

## File Metadata Schema

Each file entry contains:

```json
"path/to/file.txt": {
  "size": 1234,
  "mtime": 1732464000.0,
  "content_hash": "516ad7b388b21e05e8c56229f063d112e70a2fea45fdd357e8ff44e6a5bce689",
  "leaf_hash": "8a9f3c12d45e6b8f1a2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a"
}
```

### File Fields

#### `size` (number, required)

File size in bytes.

- **Type**: Integer
- **Example**: `1234`
- **Purpose**: Quick comparison, metadata

#### `mtime` (number, required)

File modification time.

- **Format**: Unix timestamp (seconds since epoch)
- **Example**: `1732464000.0`
- **Purpose**: Change detection hint (not cryptographically verified)

#### `content_hash` (string, required)

Raw SHA-256 hash of the file contents.

- **Format**: 64-character hexadecimal string
- **Example**: `"516ad7b388b21e05e8c56229f063d112e70a2fea45fdd357e8ff44e6a5bce689"`
- **Computation**: `SHA256(file_contents)`
- **Purpose**: File integrity verification

#### `leaf_hash` (string, required)

Merkle tree leaf node hash.

- **Format**: 64-character hexadecimal string
- **Example**: `"8a9f3c12d45e6b8f1a2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a"`
- **Computation**: `SHA256(0x00 || content_hash_bytes)`
- **Purpose**: Merkle tree construction

## Directory Metadata Schema

Each directory entry contains:

```json
"path/to/directory": {
  "root_hash": "94eee32191b256f2fdd489422beed8b7f1220e388d95d19002d7d4881c2f5fc7",
  "node_hash": "1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b"
}
```

### Directory Fields

#### `root_hash` (string, required)

Merkle root hash of the subdirectory.

- **Format**: 64-character hexadecimal string
- **Example**: `"94eee32191b256f2fdd489422beed8b7f1220e388d95d19002d7d4881c2f5fc7"`
- **Computation**: Merkle root of subdirectory's children
- **Purpose**: Subdirectory integrity

#### `node_hash` (string, required)

Directory node hash used in parent's Merkle tree.

- **Format**: 64-character hexadecimal string
- **Example**: `"1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b"`
- **Computation**: `SHA256(0x02 || root_hash_bytes)`
- **Purpose**: Parent Merkle tree construction

## Example Manifest

```json
{
  "merklewatch_version": "1.0.0",
  "algorithm": "sha256",
  "timestamp": 1732464642.123456,
  "timestamp_iso": "2025-11-24T14:50:42Z",
  "root_hash": "a7304db0e614521b6cd9c79bfaa8707f845c5f9f509bbc8286f040461b0820b9",
  "files": {
    "README.md": {
      "size": 5432,
      "mtime": 1732460000.0,
      "content_hash": "516ad7b388b21e05e8c56229f063d112e70a2fea45fdd357e8ff44e6a5bce689",
      "leaf_hash": "8a9f3c12d45e6b8f1a2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a"
    },
    "LICENSE": {
      "size": 1069,
      "mtime": 1732460000.0,
      "content_hash": "7d3e8f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9",
      "leaf_hash": "2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3"
    },
    "src/main.py": {
      "size": 2048,
      "mtime": 1732462000.0,
      "content_hash": "9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0",
      "leaf_hash": "4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5"
    }
  },
  "directories": {
    "src": {
      "root_hash": "94eee32191b256f2fdd489422beed8b7f1220e388d95d19002d7d4881c2f5fc7",
      "node_hash": "1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b"
    },
    "src/utils": {
      "root_hash": "5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6",
      "node_hash": "7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8"
    }
  }
}
```

## Path Conventions

### Relative Paths

All paths in the manifest are **relative** to the root directory being snapshotted.

- **Format**: POSIX-style paths with `/` separator
- **Root**: Paths do NOT start with `/`
- **Examples**:
  - `README.md` (file in root)
  - `src/main.py` (file in subdirectory)
  - `src` (subdirectory)
  - `src/utils` (nested subdirectory)

### Path Sorting

- **Alphabetically sorted**: For deterministic ordering
- **Case-sensitive**: `A` comes before `a`
- **Filesystem order**: Not preserved

## JSON Formatting

### Serialization Options

MerkleWatch uses:

- **Indentation**: 2 spaces
- **Sorted keys**: `True` (for determinism)
- **No trailing commas**: Standard JSON
- **UTF-8 encoding**: For international characters

### Size Considerations

Typical manifest sizes:

- **Small project** (100 files): ~20KB
- **Medium project** (1,000 files): ~200KB
- **Large project** (10,000 files): ~2MB

## Compatibility

### Forward Compatibility

Newer versions may add fields. Old parsers should ignore unknown fields.

### Backward Compatibility

Within major version (1.x.x), schema remains compatible.

Breaking changes increment major version.

## Validation

### Required Checks

When loading a manifest:

1. ✅ JSON is valid
2. ✅ All required fields present
3. ✅ `merklewatch_version` is compatible
4. ✅ `algorithm` is supported
5. ✅ Hashes are valid hex strings (64 chars for SHA-256)
6. ✅ Paths are non-empty strings

### Optional Checks

- Verify hash lengths match algorithm
- Check timestamp is reasonable
- Validate path characters

## Usage Examples

### Reading a Manifest (Python)

```python
import json

with open('manifest.json', 'r') as f:
    manifest = json.load(f)

print(f"Version: {manifest['merklewatch_version']}")
print(f"Root Hash: {manifest['root_hash']}")
print(f"Files: {len(manifest['files'])}")
print(f"Directories: {len(manifest['directories'])}")
```

### Extracting File List

```python
import json

with open('manifest.json', 'r') as f:
    manifest = json.load(f)

for path, metadata in manifest['files'].items():
    print(f"{path}: {metadata['size']} bytes, hash={metadata['content_hash'][:16]}...")
```

### Comparing Manifests

```python
import json

def load_manifest(path):
    with open(path, 'r') as f:
        return json.load(f)

old = load_manifest('old.json')
new = load_manifest('new.json')

if old['root_hash'] == new['root_hash']:
    print("Identical!")
else:
    print("Different!")
```

## Security Notes

### What's Protected

- **File contents**: Via `content_hash`
- **Directory structure**: Via Merkle tree
- **File ordering**: Via sorted Merkle construction

### What's Not Protected

- **Manifest itself**: Can be modified
  - **Solution**: Sign manifests with GPG
- **Timestamps**: Not cryptographically verified
- **Metadata tampering**: Size, mtime can be changed
  - **Solution**: Trust only hashes, not metadata

### Best Practices

1. **Sign manifests**: Use GPG or similar
2. **Secure storage**: Keep manifests offline/encrypted
3. **Access control**: Restrict manifest write access
4. **Backup manifests**: Store in multiple locations
5. **Audit logs**: Track manifest creation/modification

## Schema Evolution

### Version 1.0.0

- Initial stable release
- Basic file and directory support
- SHA-256 hashing
- Domain-separated Merkle trees

### Future Versions (Potential)

- **1.1.0**: Add optional compression metadata
- **1.2.0**: Add signature fields for GPG integration
- **2.0.0**: Support for multiple hash algorithms
- **2.1.0**: Incremental snapshot support

## References

- [Architecture Documentation](architecture.md)
- [Ignore Rules Guide](ignore-rules.md)
- [Main README](../README.md)
