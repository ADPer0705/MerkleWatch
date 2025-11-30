<div align="center">

# 🔐 MerkleWatch

### *Deterministic. Cryptographic. Tamper-Evident.*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/ADPer0705/MerkleWatch/releases)

A CLI-first integrity verification tool that creates **tamper-evident snapshots** of directory structures using **Merkle trees** and **cryptographic hashing**.

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Commands](#-commands) • [Ignore Rules](#-ignore-rules) • [Documentation](#-documentation)

</div>

---

## 🚀 Features

- **🌲 Merkle Tree Integrity** — Creates a single cryptographic root hash representing your entire directory
- **🔒 Tamper Detection** — Detects any file modifications, additions, removals, or reorderings
- **📊 Detailed Diff Views** — Visual comparison of changes with color-coded output
- **🚫 Flexible Ignore Rules** — `.merkleignore` support with gitignore-like syntax
- **⚡ Streaming Support** — Efficiently handles large files with chunked reading (64KB chunks)
- **🎯 Deterministic** — Same directory always produces the same hash (cross-platform)
- **🧩 Modular Design** — Clean separation between hashing, tree construction, and filesystem operations
- **📋 JSON Manifests** — Human-readable snapshots with complete metadata
- **🛡️ Domain Separation** — Cryptographically safe hashing with prefix-based separation
- **🔄 Snapshot Comparison** — Compare two snapshots to see what changed over time
- **🛠️ Interactive Setup** — Guided ignore rule configuration

---

## 📦 Installation

### Prerequisites

- Python 3.10 or higher

### Install from PyPI (Recommended)

```bash
pip install merklewatch
```

### Install from Source

```bash
git clone https://github.com/ADPer0705/MerkleWatch.git
cd MerkleWatch
pip install -e .
```

---

## 🚀 Quick Start

### 1. Create a Snapshot

```bash
merklewatch snapshot ./my_project --out baseline.json
```

### 2. Verify Integrity Later

```bash
merklewatch verify baseline.json ./my_project
```

### 3. Compare Two Snapshots

```bash
merklewatch diff baseline.json latest.json
```

---

## 💻 Commands

### `snapshot` - Create a Cryptographic Snapshot

Generate a tamper-evident snapshot of any directory:

```bash
merklewatch snapshot <directory> --out <manifest.json>
```

**Examples:**

```bash
# Snapshot your project
merklewatch snapshot ./my_project --out snapshot.json

# Snapshot with ignore rules (create .merkleignore first)
echo "node_modules/" > ./my_project/.merkleignore
echo "__pycache__/" >> ./my_project/.merkleignore
merklewatch snapshot ./my_project --out clean_snapshot.json
```

**Output:**
```
Snapshoting /path/to/directory...
Snapshot created successfully!
Root Hash: a7304db0e614521b6cd9c79bfaa8707f845c5f9f509bbc8286f040461b0820b9
Manifest saved to: snapshot.json
```

### `verify` - Verify Directory Integrity

Check if a directory matches a previous snapshot:

```bash
merklewatch verify <manifest.json> <directory>
```

**Successful Verification:**

```bash
merklewatch verify baseline.json ./my_project
```

```
Verifying /path/to/directory against baseline.json...

✓ Verification SUCCESSFUL!
Root Hash matches: a7304db0e614521b6cd9c79bfaa8707f845c5f9f509bbc8286f040461b0820b9
```

**Failed Verification (Tampering Detected):**

```bash
merklewatch verify baseline.json ./my_project
```

```
Verifying /path/to/directory against baseline.json...

✗ Verification FAILED!

Root Hash Mismatch:
  Expected: a7304db0e614521b6cd9c79bfaa8707f845c5f9f509bbc8286f040461b0820b9
  Actual:   94eee32191b256f2fdd489422beed8b7f1220e388d95d19002d7d4881c2f5fc7

Summary: 3 changes: 1 added, 1 removed, 1 modified

✓ Added files:
  + new_suspicious_file.txt

✗ Removed files:
  - important_config.txt

⚠ Modified files:
  M critical_data.json
      Old: 516ad7b388b21e05e8c56229f063d112e70a2fea45fdd357e8ff44e6a5bce689
      New: 52b3272721ffd27d6300389fb9b01a86148447fc78c14f7afde337854cc0860e
```

### `diff` - Compare Two Snapshots

Compare two manifest files to see what changed between snapshots:

```bash
merklewatch diff <old_manifest.json> <new_manifest.json>
```

**Example:**

```bash
merklewatch diff snapshot_jan.json snapshot_feb.json
```

```
Comparing snapshot_jan.json → snapshot_feb.json...

Old manifest: 2025-01-15T10:30:00Z
  Root Hash: a7304db0e614521b6cd9c79bfaa8707f845c5f9f509bbc8286f040461b0820b9

New manifest: 2025-02-15T14:45:00Z
  Root Hash: 94eee32191b256f2fdd489422beed8b7f1220e388d95d19002d7d4881c2f5fc7

Summary: 5 changes: 2 added, 1 removed, 2 modified

✓ Added files:
  + src/new_feature.py
  + docs/api.md

✗ Removed files:
  - deprecated/old_code.py

⚠ Modified files:
  M src/main.py
      Old: 516ad7b388b21e05e8c56229f063d112e70a2fea45fdd357e8ff44e6a5bce689
      New: 52b3272721ffd27d6300389fb9b01a86148447fc78c14f7afde337854cc0860e
  M README.md
      Old: 8f4d3a1c9e7b2f6a5d0c8e1b4a7d3f9c2e5b8a1d4c7f0e3b6a9d2c5f8e1b4a7
      New: 1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z7a8b9c0d1e2f
```

### `ignore` - Configure Ignore Rules

Interactively configure `.merkleignore` file with a guided interface:

```bash
merklewatch ignore <directory>
```

**Interactive Prompts:**

1. **Suggests Common Patterns**: Automatically finds `node_modules/`, `.git/`, `__pycache__/`, etc.
2. **Checkbox Selection**: Check/uncheck patterns to add
3. **Browse All Files**: Optional fuzzy-searchable list of all files and directories
4. **Save**: Writes selected patterns to `.merkleignore`

**Example Session:**

```bash
merklewatch ignore ./my_project
```

```
Configuring ignores for /path/to/my_project

? Found common ignore candidates. Select ones to add: (Use arrow keys to move, space to select, type to filter)
 » ✓ node_modules/
   ✓ __pycache__/
   ✓ .git/
   ○ .DS_Store

? Do you want to browse and ignore other files/directories? (Y/n)

Updated .merkleignore with 3 new patterns.
```

---

## 🚫 Ignore Rules

MerkleWatch supports `.merkleignore` files with gitignore-like syntax. Place a `.merkleignore` file in the root of the directory you want to snapshot.

### `.merkleignore` Syntax

```gitignore
# Comments start with #

# Ignore specific files
.DS_Store
secrets.txt
config.local.json

# Ignore file patterns (glob matching)
*.log
*.tmp
*.pyc
*.swp

# Ignore directories (trailing slash recommended)
node_modules/
__pycache__/
.git/
dist/
build/
venv/

# Ignore directories (without slash also works)
.env
cache
temp
```

### Pattern Matching Rules

| Pattern Type | Example | Matches |
|-------------|---------|---------|
| **Directory** (with `/`) | `node_modules/` | Directory and all its contents |
| **Directory** (without `/`) | `build` | Any file/directory named `build` |
| **Glob pattern** | `*.log` | All files ending with `.log` anywhere |
| **Specific file** | `.DS_Store` | Exact filename match anywhere |
| **Comment** | `# ignore logs` | Ignored (documentation) |

### Important Notes

- ⚠️ **No Built-in Ignores**: MerkleWatch has NO default ignore patterns. Only patterns in `.merkleignore` are used.
- 📝 **Create Before Snapshot**: Place `.merkleignore` before running `snapshot`
- 🔄 **Applies to All Commands**: Both `snapshot` and `verify` respect ignore rules
- 🎯 **Case Sensitive**: Pattern matching is case-sensitive

---

## 🏗️ How It Works

MerkleWatch creates a **cryptographically secure fingerprint** of your directory structure using Merkle trees:

### 1️⃣ Hash Every File

Files are hashed using SHA-256 with chunked reading (64KB chunks) to handle large files efficiently:

```
file_hash = SHA256(file_contents)
leaf_hash = SHA256(0x00 || file_hash)
```

### 2️⃣ Build Merkle Trees

Each directory becomes a Merkle tree where:
- Files are **leaf nodes** (prefixed with `0x00`)
- Subdirectories are represented by their **root hash** (prefixed with `0x02`)
- All children are **sorted alphabetically** and paired

```
internal_hash = SHA256(0x01 || left || right)
dir_node = SHA256(0x02 || subdirectory_root_hash)
```

### 3️⃣ Compute Root Hash

The entire directory structure collapses into a **single root hash** — your tamper-evident seal.

```
Root Hash = MerkleRoot(all children)
```

### Domain Separation

| Type | Prefix | Purpose |
|------|--------|---------|
| File leaf | `0x00` | Content leaf |
| Internal node | `0x01` | Combines two children |
| Directory node | `0x02` | Represents subdirectory root |

This prevents **second-preimage attacks** and ensures cryptographic safety.

---

## 📋 Manifest Format

Manifests are JSON files containing:

```json
{
  "merklewatch_version": "1.0.0",
  "algorithm": "sha256",
  "timestamp": 1732464642.123456,
  "timestamp_iso": "2025-11-24T14:50:42Z",
  "root_hash": "a7304db0e614521b6cd9c79bfaa8707f845c5f9f509bbc8286f040461b0820b9",
  "files": {
    "README.md": {
      "size": 1234,
      "mtime": 1732464000.0,
      "content_hash": "516ad7b388b21...",
      "leaf_hash": "8a9f3c12d45..."
    }
  },
  "directories": {
    "src": {
      "root_hash": "94eee32191b256...",
      "node_hash": "1a2b3c4d5e6f..."
    }
  }
}
```

See [`docs/manifest-format.md`](docs/manifest-format.md) for full specification.

---

## 🗂️ Project Structure

```
merklewatch/
├── src/merklewatch/
│   ├── __init__.py         # Package initialization
│   ├── __main__.py         # Entry point
│   ├── cli.py              # Typer-based CLI interface
│   ├── hashing.py          # SHA-256 primitives with domain separation
│   ├── merkle.py           # Merkle tree construction logic
│   ├── filesystem.py       # Directory traversal & scanning
│   ├── manifest.py         # JSON manifest generation
│   ├── verification.py     # Verification logic
│   ├── diff.py             # Diff formatting and display
│   └── ignore.py           # Ignore rules handling
├── docs/                   # Documentation
│   ├── architecture.md     # System architecture
│   ├── manifest-format.md  # Manifest specification
│   ├── ignore-rules.md     # Ignore rules guide
│   └── examples.md         # Usage examples
├── test/                   # Test data
├── pyproject.toml          # Project metadata & dependencies
├── Makefile                # Development automation
├── CHANGELOG.md            # Version history
├── CONTRIBUTING.md         # Contribution guidelines
├── LICENSE                 # MIT License
└── README.md               # This file
```

---

## 🛠️ Error Handling

MerkleWatch gracefully handles common filesystem issues:

- **Permission Errors**: Warns and skips inaccessible files/directories
- **Symlinks**: Skips symbolic links to avoid loops and security issues
- **Empty Directories**: Handles empty directories correctly
- **Large Files**: Uses chunked reading (64KB) to avoid memory issues
- **Missing Files**: During verification, clearly reports added/removed files

---

## 🎯 Use Cases

- **🔍 Digital Forensics** — Chain-of-custody documentation with tamper-evident snapshots
- **🔐 Security Audits** — Verify configuration integrity across systems
- **💾 Backup Verification** — Ensure backup completeness and detect corruption
- **🏗️ Reproducible Builds** — Verify build outputs match expected state
- **📊 File System Monitoring** — Detect unauthorized changes in critical directories
- **📦 Software Distribution** — Verify package integrity before deployment
- **🔄 Change Tracking** — Track changes between versions with detailed diffs

---

## 📚 Documentation

- [Installation Guide](#-installation)
- [Quick Start](#-quick-start)
- [Commands Reference](#-commands)
- [Ignore Rules Guide](#-ignore-rules)
- [Architecture Documentation](docs/architecture.md)
- [Manifest Format Specification](docs/manifest-format.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)
- [License](LICENSE)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Inspired by the need for deterministic, cryptographically secure directory integrity verification in:
- Digital forensics workflows
- Secure backup systems
- Configuration management
- Reproducible build systems

---

<div align="center">

**Made with ❤️ by [ADPer](https://github.com/ADPer0705)**

⭐ Star this repo if you find it useful!

[Report Bug](https://github.com/ADPer0705/MerkleWatch/issues) · [Request Feature](https://github.com/ADPer0705/MerkleWatch/issues)

</div>
