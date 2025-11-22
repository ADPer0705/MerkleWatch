<div align="center">

# 🔐 MerkleWatch

### *Deterministic. Cryptographic. Tamper-Evident.*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-0.1.0-green.svg)](https://github.com/ADPer0705/MerkleWatch/releases)

A CLI-first integrity verification tool that creates **tamper-evident snapshots** of directory structures using **Merkle trees** and **cryptographic hashing**.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 🚀 Features

- **🌲 Merkle Tree Integrity** — Creates a single cryptographic root hash representing your entire directory
- **🔒 Tamper Detection** — Detects any file modifications, additions, removals, or reorderings
- **⚡ Streaming Support** — Efficiently handles large files with chunked reading
- **🎯 Deterministic** — Same directory always produces the same hash (cross-platform)
- **🧩 Modular Design** — Clean separation between hashing, tree construction, and filesystem operations
- **📋 JSON Manifests** — Human-readable snapshots with complete metadata
- **🛡️ Domain Separation** — Cryptographically safe hashing with prefix-based separation

---

## 📦 Installation

### Prerequisites

- Python 3.10 or higher

### Install from source

```bash
git clone https://github.com/ADPer0705/MerkleWatch.git
cd MerkleWatch
pip install -e .
```

---

## 💻 Usage

### Create a Snapshot

Generate a cryptographic snapshot of any directory:

```bash
merklewatch snapshot <directory_path> --out manifest.json
```

**Example:**

```bash
merklewatch snapshot ./my_important_data --out snapshot_2025.json
```

**Output:**
```
Snapshoting /path/to/directory...
Snapshot created successfully!
Root Hash: a7304db0e614521b6cd9c79bfaa8707f845c5f9f509bbc8286f040461b0820b9
Manifest saved to: snapshot_2025.json
```

### Verify a Snapshot

*Note: Full verification is coming in v0.2.0*

```bash
merklewatch verify snapshot_2025.json ./my_important_data
```

---

## 🏗️ How It Works

MerkleWatch creates a **cryptographically secure fingerprint** of your directory structure:

### 1️⃣ Hash Every File

```
file_hash = SHA256(file_contents)
leaf_hash = SHA256(0x00 || file_hash)
```

### 2️⃣ Build Merkle Trees

Each directory becomes a Merkle tree where:
- Files are leaf nodes
- Subdirectories are represented by their root hash
- All children are sorted and paired

```
internal_hash = SHA256(0x01 || left || right)
dir_node = SHA256(0x02 || subdirectory_root_hash)
```

### 3️⃣ Compute Root Hash

The entire directory structure collapses into a **single root hash** — your tamper-evident seal.

### Domain Separation

| Type                 | Prefix | Purpose                          |
|---------------------|--------|----------------------------------|
| File leaf           | `0x00` | Content leaf                     |
| Internal node       | `0x01` | Combines two children            |
| Directory node      | `0x02` | Represents subdirectory root     |

This prevents **second-preimage attacks** and ensures cryptographic safety.

---

## 🗂️ Project Structure

```
merklewatch/
├── src/merklewatch/
│   ├── hashing.py          # SHA-256 primitives with domain separation
│   ├── merkle.py           # Merkle tree construction logic
│   ├── filesystem.py       # Directory traversal & scanning
│   ├── manifest.py         # JSON manifest generation
│   ├── cli.py              # Typer-based CLI interface
│   └── __init__.py
├── docs/                   # Documentation (coming soon)
├── pyproject.toml          # Project metadata & dependencies
├── Makefile                # Development automation
└── README.md
```

---

## 🛠️ Development

### Setup Development Environment

```bash
make dev
```

### Available Make Commands

| Command                                      | Description                          |
|---------------------------------------------|--------------------------------------|
| `make help`                                  | Show all available commands          |
| `make install`                               | Install package in editable mode     |
| `make dev`                                   | Install development dependencies     |
| `make clean`                                 | Remove build artifacts & cache       |
| `make snapshot DIR=... OUT=...`              | Create a snapshot                    |
| `make verify MANIFEST=... DIR=...`           | Verify a snapshot                    |
| `make lint`                                  | Run code linters                     |
| `make format`                                | Format code with Black               |
| `make docs`                                  | Build documentation                  |
| `make docs-serve`                            | Serve docs locally                   |

### Example Workflow

```bash
# Setup
make dev

# Format code
make format

# Run linting
make lint

# Create a test snapshot
make snapshot DIR=./src OUT=test_manifest.json
```

---

## 📚 Documentation

### Quick Links
- [Contributing Guide](CONTRIBUTING.md)
- [License](LICENSE)
- [Changelog](https://github.com/ADPer0705/MerkleWatch/releases)

### Core Concepts

**Merkle Trees**: Each directory is represented as a Merkle tree where files are leaves and subdirectories are represented by their root hashes. The entire structure collapses into a single root hash.

**Domain Separation**: We use prefix bytes (`0x00`, `0x01`, `0x02`) to cryptographically separate different node types, preventing second-preimage attacks.

**Deterministic Hashing**: Files are read in chunks, children are sorted alphabetically, and the algorithm is platform-independent, ensuring reproducible results.

---

## 🎯 Use Cases

- **Digital Forensics** — Chain-of-custody documentation
- **Security Audits** — Verify configuration integrity
- **Backup Verification** — Ensure backup completeness
- **Reproducible Builds** — Verify build outputs
- **File System Monitoring** — Detect unauthorized changes

---

## 🗺️ Roadmap

- [x] **v0.1.0** — Snapshot generation with Merkle trees
- [ ] **v0.2.0** — Full verification logic
- [ ] **v0.3.0** — Alert system for changes
- [ ] **v0.4.0** — Incremental snapshots & proofs
- [ ] **v0.5.0** — Signing & verification with GPG

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

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

</div>
