# Ignore Rules Guide

## Overview

MerkleWatch supports `.merkleignore` files for excluding files and directories from snapshots. The syntax is similar to `.gitignore`.

## Basic Usage

1. Create a `.merkleignore` file in the root of the directory you want to snapshot
2. Add patterns (one per line)
3. Run `merklewatch snapshot` - ignored files are automatically excluded

## Syntax

### Comments

Lines starting with `#` are comments:

```gitignore
# This is a comment
# Ignore build artifacts
```

### Blank Lines

Empty lines are ignored:

```gitignore
*.log

# Group separator

*.tmp
```

### Directory Patterns

Ignore directories and all their contents:

```gitignore
node_modules/
__pycache__/
.git/
dist/
build/
```

**Note**: Trailing slash `/` is recommended for clarity but optional.

### File Patterns

Ignore specific files:

```gitignore
.DS_Store
Thumbs.db
.env
secrets.txt
```

### Glob Patterns

Use wildcards for pattern matching:

```gitignore
# All log files
*.log

# All Python cache files
*.pyc

# All temporary files
*.tmp
*.swp

# All files starting with 'test_'
test_*
```

### Wildcard Characters

| Character | Meaning | Example | Matches |
|-----------|---------|---------|---------|
| `*` | Any characters | `*.txt` | `file.txt`, `test.txt` |
| `?` | Single character | `?.log` | `a.log`, `1.log` |
| `[abc]` | Character class | `[0-9].txt` | `1.txt`, `2.txt` |

## Pattern Matching Rules

### Directory Matching

Pattern `node_modules/` matches:
- ✅ `node_modules/` (the directory itself)
- ✅ `node_modules/package.json` (files inside)
- ✅ `node_modules/lib/index.js` (nested files)

### Simple Name Matching

Pattern `build` (without `/` or wildcard) matches:
- ✅ `build/` (directory in root)
- ✅ `src/build/` (directory anywhere)
- ✅ `build` (file in root)
- ✅ `src/build` (file anywhere)

### Glob Matching

Pattern `*.log` matches:
- ✅ `error.log` (in root)
- ✅ `logs/error.log` (in subdirectory)
- ✅ `src/app.log` (anywhere)

## Examples

### Python Project

```gitignore
# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd

# Virtual environments
venv/
env/
.venv/

# IDE
.vscode/
.idea/
*.swp

# Build
dist/
build/
*.egg-info/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Environment
.env
.env.local
```

### Node.js Project

```gitignore
# Dependencies
node_modules/

# Build output
dist/
build/
.next/
out/

# IDE
.vscode/
.idea/

# Environment
.env
.env.local
.env.production

# Logs
*.log
npm-debug.log*

# OS
.DS_Store
Thumbs.db
```

### General Purpose

```gitignore
# Version control
.git/
.svn/

# OS files
.DS_Store
Thumbs.db
desktop.ini

# Logs
*.log
logs/

# Temporary files
*.tmp
*.temp
*.swp
*~

# Archives
*.zip
*.tar.gz
*.rar
```

## Interactive Configuration

Use the `ignore` command for guided setup:

```bash
merklewatch ignore <directory>
```

This will:
1. Scan for common patterns (node_modules/, .git/, etc.)
2. Let you select which to add
3. Optionally browse all files/directories
4. Save selections to `.merkleignore`

## How It Works

### Ignore Rule Application

1. MerkleWatch reads `.merkleignore` from the snapshot root
2. During directory scanning, each file/directory is checked against patterns
3. Matching paths are skipped (not hashed, not included in manifest)

### Pattern Evaluation

For each path, MerkleWatch:
1. Converts path to POSIX format (`/` separators)
2. Checks each pattern in order
3. If any pattern matches, path is ignored
4. If no patterns match, path is included

### Performance

- Patterns are evaluated once per file/directory
- No regex compilation overhead (uses fnmatch)
- Ignored directories are not traversed (saves time)

## Important Notes

### No Built-in Ignores

⚠️ **MerkleWatch has NO default ignore patterns.**

If you don't create a `.merkleignore` file, **everything** is included:
- `.git/` directories
- `node_modules/`
- `__pycache__/`
- etc.

### Case Sensitivity

Pattern matching is **case-sensitive**:
- `*.log` matches `error.log` but NOT `ERROR.LOG`
- `Build/` matches `Build/` but NOT `build/`

### Both Snapshot and Verify

Ignore rules apply to:
- ✅ `merklewatch snapshot` (exclude from snapshot)
- ✅ `merklewatch verify` (exclude from verification)

This ensures consistency.

### Path Relativity

Patterns match against paths **relative to the snapshot root**:

```
project/
├── .merkleignore
├── build/         # Matched by "build/"
├── src/
│   └── build/     # Also matched by "build/"
```

## Troubleshooting

### Pattern Not Working

1. **Check file exists**: `.merkleignore` must be in snapshot root
2. **Check syntax**: One pattern per line, no quotes
3. **Check path**: Pattern must match relative path
4. **Check spelling**: Typos won't match
5. **Test**: Create test file and check if ignored

### Ignoring Too Much

1. **Review patterns**: Check for overly broad wildcards
2. **Remove patterns**: Edit `.merkleignore` and remove lines
3. **Test**: Run snapshot and verify expected files included

### Pattern Examples

```gitignore
# ✅ Good patterns
*.log              # All log files
node_modules/      # Node modules directory
.git/              # Git directory
test_*.py          # Python test files

# ❌ Common mistakes
"*.log"            # Don't use quotes
*.log;             # Don't use semicolons
/node_modules/     # Don't use leading slash (not needed)
```

## Best Practices

1. **Start with common patterns**: Use `merklewatch ignore` to find common ignores
2. **Comment your patterns**: Explain why things are ignored
3. **Group related patterns**: Use blank lines to separate groups
4. **Be specific**: Avoid overly broad wildcards
5. **Test your ignores**: Run snapshot and check file count makes sense
6. **Version control**: Commit `.merkleignore` to your repository
7. **Document exceptions**: Note any unusual ignore patterns

## Advanced Usage

### Negation (Not Supported)

MerkleWatch does NOT support negation patterns like `!important.log`.

**Workaround**: Be explicit about what to ignore.

### Directory-Specific Ignores (Not Supported)

Only root-level `.merkleignore` is used. Subdirectory `.merkleignore` files are ignored.

**Workaround**: Put all patterns in root `.merkleignore`.

### Anchoring (Not Supported)

Patterns match anywhere in the path (no `/` anchoring like gitignore).

**Workaround**: Use more specific patterns.

## FAQ

**Q: Does `.merkleignore` itself get included in snapshots?**  
A: No, `.merkleignore` is automatically excluded.

**Q: Can I have multiple `.merkleignore` files?**  
A: No, only the one in the snapshot root is used.

**Q: What if I don't have a `.merkleignore`?**  
A: Everything is included (no default ignores).

**Q: Can I use regex patterns?**  
A: No, only simple globs (`*`, `?`, `[...]`).

**Q: Are patterns case-sensitive?**  
A: Yes, pattern matching is case-sensitive.

**Q: Can I ignore everything except some files?**  
A: No, whitelist patterns are not supported. Only blacklist (ignore) patterns.

## See Also

- [Main README](../README.md)
- [Architecture](architecture.md)
- [Manifest Format](manifest-format.md)
