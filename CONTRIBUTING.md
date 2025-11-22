# Contributing to MerkleWatch

Thank you for your interest in contributing to MerkleWatch! This document provides guidelines and instructions for contributing.

## Getting Started

### Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/MerkleWatch.git
   cd MerkleWatch
   ```

3. Install development dependencies:
   ```bash
   make dev
   ```

## Development Workflow

### Making Changes

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes
3. Format your code:
   ```bash
   make format
   ```

4. Run linting:
   ```bash
   make lint
   ```

5. Test your changes manually:
   ```bash
   make snapshot DIR=./test_data OUT=test.json
   ```

### Commit Messages

Use clear and descriptive commit messages:
- `feat: add verification command`
- `fix: handle empty directories correctly`
- `docs: update README installation instructions`
- `refactor: simplify merkle tree construction`

### Pull Request Process

1. Update the README.md if needed
2. Ensure all linting passes
3. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
4. Open a Pull Request with a clear description of your changes

## Code Style

- Follow PEP 8 guidelines
- Use Black for formatting (automatically done with `make format`)
- Use type hints where appropriate
- Keep functions small and focused
- Add docstrings to functions and classes

## Project Structure

```
src/merklewatch/
├── hashing.py      # Cryptographic primitives
├── merkle.py       # Merkle tree logic
├── filesystem.py   # Directory scanning
├── manifest.py     # JSON manifest handling
└── cli.py          # CLI interface
```

## Feature Requests

Have an idea? Open an issue with:
- Clear description of the feature
- Use cases
- Example usage (if applicable)

## Bug Reports

Found a bug? Open an issue with:
- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version)

## Questions?

Feel free to open an issue for questions or discussions!
