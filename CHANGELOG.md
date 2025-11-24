# Changelog

All notable changes to MerkleWatch will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-24

### Added
- **Production-ready release** with comprehensive error handling
- Robust error handling for permission errors, symlinks, and filesystem issues
- Detailed warning messages for inaccessible files/directories
- Graceful handling of empty directories
- Comprehensive documentation in `docs/` directory:
  - `architecture.md` - System architecture and design
  - `manifest-format.md` - Complete manifest specification
  - `ignore-rules.md` - Ignore rules guide
  - `examples.md` - Usage examples and workflows
- Updated README.md with complete usage guide
- All features from v0.1.0 - v0.4.0 stabilized

### Changed
- Improved filesystem scanning with better error recovery
- Enhanced `hash_file()` with explicit error handling
- Symlinks are now skipped with warnings (security improvement)
- Permission errors no longer crash the application
- Empty directories handled correctly in Merkle tree construction

### Fixed
- Edge cases in error handling during directory traversal
- Proper cleanup when encountering inaccessible files

## [0.4.0] - 2025-11-24

### Added
- **Ignore rules support** with `.merkleignore` files
- New `ignore` command for interactive ignore configuration
- `IgnoreRules` class for pattern matching (gitignore-like syntax)
- Support for directory patterns (`node_modules/`), globs (`*.log`), and simple names
- Interactive file browser with `questionary` for selecting ignores
- Automatic suggestion of common ignore patterns
- Integration with `snapshot` and `verify` commands

### Changed
- `filesystem.py` updated to respect ignore rules
- `verification.py` updated to use ignore rules during verification
- Added `questionary>=2.0.0` dependency

### Documentation
- Added ignore rules section to README
- No built-in ignores - user must create `.merkleignore`

## [0.3.0] - 2025-11-24

### Added
- **Detailed diff views** for verification and manifest comparison
- New `diff` command to compare two manifest files
- Enhanced `verify` command with color-coded diff output
- `diff.py` module with formatting utilities:
  - `display_added_files()` - Green colored output
  - `display_removed_files()` - Red colored output
  - `display_modified_files_detailed()` - Yellow with hash details
  - `display_verification_diff()` - Verification-specific formatting
- Visual indicators (✓, ✗, ⚠) for different change types
- Old vs new hash comparison for modified files

### Changed
- `verification.py` now returns detailed file metadata
- `verify` command shows comprehensive diff instead of simple file list
- Exit code 1 for `diff` command when differences found (Unix convention)

### Fixed
- Better diff presentation with summary statistics

## [0.2.0] - 2025-11-24

### Added
- **Full verification logic** for directory integrity checking
- `verification.py` module with:
  - `verify_directory()` - Complete verification workflow
  - `compare_manifests()` - Detailed comparison logic
  - `load_manifest()` - Manifest loading utility
- Detection of added, removed, and modified files
- Verification command shows which files changed

### Changed
- Verification now provides detailed feedback
- Root hash comparison with file-level details

## [0.1.0] - 2025-11-24

### Added
- Initial release of MerkleWatch
- Core Merkle tree implementation
- SHA-256 hashing with domain separation
- Directory snapshotting functionality
- JSON manifest generation
- CLI interface with `snapshot` command
- Deterministic hash computation
- Chunked file reading for large files (64KB chunks)
- Modular architecture:
  - `hashing.py` - Cryptographic primitives
  - `merkle.py` - Merkle tree construction
  - `filesystem.py` - Directory traversal
  - `manifest.py` - Manifest creation
  - `cli.py` - Command-line interface

### Features
- Create cryptographic snapshots of directories
- Domain separation for different node types (0x00, 0x01, 0x02)
- Sorted, deterministic tree construction
- Human-readable JSON manifests with metadata
- Cross-platform compatibility

## [Unreleased]

### Planned Features
- Parallel/threaded hashing for performance
- Progress bars for large directory operations
- Automated testing suite
- GPG signing integration for manifests
- Incremental snapshots
- Watch mode for continuous monitoring
- Web UI for visualization
- Compression for large manifests

---

## Version History Summary

| Version | Date | Key Feature |
|---------|------|-------------|
| 1.0.0 | 2025-11-24 | Production release with error handling & docs |
| 0.4.0 | 2025-11-24 | Ignore rules support |
| 0.3.0 | 2025-11-24 | Diff views and comparison |
| 0.2.0 | 2025-11-24 | Verification logic |
| 0.1.0 | 2025-11-24 | Initial release |

---

## Links

- [Repository](https://github.com/ADPer0705/MerkleWatch)
- [Issues](https://github.com/ADPer0705/MerkleWatch/issues)
- [Releases](https://github.com/ADPer0705/MerkleWatch/releases)

[1.0.0]: https://github.com/ADPer0705/MerkleWatch/releases/tag/v1.0.0
[0.4.0]: https://github.com/ADPer0705/MerkleWatch/releases/tag/v0.4.0
[0.3.0]: https://github.com/ADPer0705/MerkleWatch/releases/tag/v0.3.0
[0.2.0]: https://github.com/ADPer0705/MerkleWatch/releases/tag/v0.2.0
[0.1.0]: https://github.com/ADPer0705/MerkleWatch/releases/tag/v0.1.0
