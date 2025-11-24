# Usage Examples

## Common Use Cases

### 1. Software Project Integrity

Track changes in your codebase over time.

```bash
# Initial snapshot
merklewatch snapshot ./myproject --out baseline.json

# After making changes
merklewatch snapshot ./myproject --out after-refactor.json

# See what changed
merklewatch diff baseline.json after-refactor.json
```

### 2. Backup Verification

Ensure backups are complete and unmodified.

```bash
# Before backup
merklewatch snapshot /important/data --out pre-backup.json

# After restore
merklewatch verify pre-backup.json /restored/data
```

### 3. Configuration Auditing

Detect unauthorized configuration changes.

```bash
# Snapshot production config
merklewatch snapshot /etc/myapp --out prod-config.json

# Weekly check
merklewatch verify prod-config.json /etc/myapp
```

### 4. Digital Forensics

Create tamper-evident evidence snapshots.

```bash
# At scene
merklewatch snapshot /evidence --out scene-$(date +%Y%m%d-%H%M%S).json

# Later verification
merklewatch verify scene-20251124-143000.json /evidence
```

### 5. Release Verification

Verify software distribution packages.

```bash
# Create official release snapshot
merklewatch snapshot ./release-v1.0 --out official-v1.0.json

# User verifies downloaded package
merklewatch verify official-v1.0.json ./downloaded
```

## Workflow Examples

### Daily Monitoring

```bash
#!/bin/bash
# daily-check.sh

DIR="/critical/files"
BASELINE="baseline.json"
DATE=$(date +%Y-%m-%d)

# Verify against baseline
if merklewatch verify "$BASELINE" "$DIR"; then
    echo "$DATE: ✓ No changes detected"
else
    echo "$DATE: ✗ CHANGES DETECTED!"
    # Send alert
    mail -s "File changes detected" admin@example.com < /dev/null
fi
```

### Version Comparison

```bash
#!/bin/bash
# compare-releases.sh

V1="./release-1.0"
V2="./release-1.1"

# Snapshot both versions
merklewatch snapshot "$V1" --out v1.0.json
merklewatch snapshot "$V2" --out v1.1.json

# Compare
merklewatch diff v1.0.json v1.1.json > changelog.txt

echo "Changes written to changelog.txt"
```

### Automated Backup Validation

```bash
#!/bin/bash
# backup-verify.sh

SOURCE="/data"
BACKUP="/backup/data"
MANIFEST="/backup/manifest-$(date +%Y%m%d).json"

# Create snapshot of source
merklewatch snapshot "$SOURCE" --out "$MANIFEST"

# Run backup (your backup tool here)
rsync -a "$SOURCE/" "$BACKUP/"

# Verify backup
if merklewatch verify "$MANIFEST" "$BACKUP"; then
    echo "✓ Backup verified successfully"
else
    echo "✗ Backup verification FAILED"
    exit 1
fi
```

## Ignore Rule Examples

### Python Project

```bash
cd myproject

# Create ignore file
cat > .merkleignore << 'EOF'
# Python
__pycache__/
*.pyc
venv/
.pytest_cache/

# IDE
.vscode/
.idea/

# Build
dist/
build/
*.egg-info/
EOF

# Snapshot clean project
merklewatch snapshot . --out project.json
```

### Node.js Project

```bash
cd webapp

# Interactive setup
merklewatch ignore .

# Manual additions
echo "coverage/" >> .merkleignore
echo ".env.local" >> .merkleignore

# Snapshot
merklewatch snapshot . --out webapp-snapshot.json
```

### System Configuration

```bash
cd /etc

# Create ignore for volatile files
cat > .merkleignore << 'EOF'
# Ignore volatile files
*.pid
*.sock
*.log
machine-id
hostname
EOF

# Snapshot configuration
merklewatch snapshot . --out etc-snapshot.json
```

## Integration Examples

### Git Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Create snapshot before commit
merklewatch snapshot . --out .git/pre-commit-snapshot.json

# Store hash in commit message template
HASH=$(jq -r '.root_hash' .git/pre-commit-snapshot.json)
echo "Snapshot: $HASH" >> .git/COMMIT_EDITMSG
```

### CI/CD Pipeline

```yaml
# .github/workflows/verify.yml
name: Verify Build

on: [push]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install MerkleWatch
        run: pip install merklewatch
      
      - name: Create snapshot
        run: merklewatch snapshot ./dist --out dist-snapshot.json
      
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: snapshot
          path: dist-snapshot.json
```

### Cron Job Monitoring

```bash
# /etc/cron.daily/merklewatch-check

#!/bin/bash
DIRS=("/var/www" "/etc/nginx" "/etc/ssl")
BASELINE_DIR="/var/merklewatch/baselines"
LOG="/var/log/merklewatch.log"

for dir in "${DIRS[@]}"; do
    name=$(basename "$dir")
    baseline="$BASELINE_DIR/$name.json"
    
    if [ ! -f "$baseline" ]; then
        echo "Creating baseline for $dir"
        merklewatch snapshot "$dir" --out "$baseline"
    else
        if ! merklewatch verify "$baseline" "$dir" >> "$LOG" 2>&1; then
            echo "ALERT: Changes detected in $dir" | mail -s "MerkleWatch Alert" admin@example.com
        fi
    fi
done
```

## Advanced Usage

### Multiple Snapshots for History

```bash
#!/bin/bash
# Keep 30 days of snapshots

DIR="/important/data"
SNAPSHOT_DIR="./snapshots"
DATE=$(date +%Y%m%d)

mkdir -p "$SNAPSHOT_DIR"

# Create daily snapshot
merklewatch snapshot "$DIR" --out "$SNAPSHOT_DIR/snapshot-$DATE.json"

# Delete snapshots older than 30 days
find "$SNAPSHOT_DIR" -name "snapshot-*.json" -mtime +30 -delete
```

### Comparing Multiple Versions

```bash
#!/bin/bash
# Compare a series of snapshots

SNAPSHOTS=("v1.0.json" "v1.1.json" "v1.2.json" "v2.0.json")

for ((i=0; i<${#SNAPSHOTS[@]}-1; i++)); do
    old="${SNAPSHOTS[$i]}"
    new="${SNAPSHOTS[$i+1]}"
    
    echo "=== Changes from $old to $new ==="
    merklewatch diff "$old" "$new"
    echo
done
```

### Selective Verification

```bash
#!/bin/bash
# Verify only specific subdirectories

BASE_MANIFEST="full-snapshot.json"
SUBDIRS=("src" "docs" "config")

for subdir in "${SUBDIRS[@]}"; do
    echo "Checking $subdir..."
    
    # Extract subdir manifest (requires jq)
    jq ".files | to_entries | map(select(.key | startswith(\"$subdir/\"))) | from_entries" \
        "$BASE_MANIFEST" > "temp-$subdir.json"
    
    # Would need custom verification logic here
    # This is示意 - actual implementation would be more complex
done
```

## Output Parsing

### Extract Root Hash

```bash
# Using jq
merklewatch snapshot ./mydir --out snapshot.json
ROOT_HASH=$(jq -r '.root_hash' snapshot.json)
echo "Root hash: $ROOT_HASH"
```

### List All Files

```bash
# List files with sizes
jq -r '.files | to_entries[] | "\(.key): \(.value.size) bytes"' snapshot.json
```

### Find Large Files

```bash
# Files larger than 1MB
jq -r '.files | to_entries[] | select(.value.size > 1048576) | "\(.key): \(.value.size)"' snapshot.json
```

### Compare File Counts

```bash
# Count files in two snapshots
COUNT1=$(jq '.files | length' snapshot1.json)
COUNT2=$(jq '.files | length' snapshot2.json)
echo "Snapshot 1: $COUNT1 files"
echo "Snapshot 2: $COUNT2 files"
echo "Difference: $((COUNT2 - COUNT1)) files"
```

## Troubleshooting Examples

### Debug Ignore Rules

```bash
# Create test directory
mkdir test-ignore
cd test-ignore
echo "test" > file1.txt
mkdir ignored-dir
echo "test" > ignored-dir/file2.txt

# Create ignore
echo "ignored-dir/" > .merkleignore

# Snapshot and check
merklewatch snapshot . --out test.json
jq '.files | keys' test.json

# Should only see file1.txt, not ignored-dir/file2.txt
```

### Find Missing Files

```bash
# Compare manifest to filesystem
jq -r '.files | keys[]' baseline.json | while read file; do
    if [ ! -f "$file" ]; then
        echo "Missing: $file"
    fi
done
```

### Verify Specific File

```bash
# Check if specific file changed
FILE="important.txt"
MANIFEST="baseline.json"

EXPECTED=$(jq -r ".files[\"$FILE\"].content_hash" "$MANIFEST")
ACTUAL=$(sha256sum "$FILE" | awk '{print $1}')

if [ "$EXPECTED" = "$ACTUAL" ]; then
    echo "✓ $FILE unchanged"
else
    echo "✗ $FILE MODIFIED"
    echo "  Expected: $EXPECTED"
    echo "  Actual:   $ACTUAL"
fi
```

## Best Practices

### 1. Regular Snapshots

```bash
# Weekly snapshots
0 0 * * 0 /usr/local/bin/merklewatch snapshot /data --out /backups/weekly-$(date +\%Y\%W).json
```

### 2. Secure Storage

```bash
# Encrypt manifests
merklewatch snapshot /data --out snapshot.json
gpg --encrypt --recipient admin@example.com snapshot.json
rm snapshot.json
```

### 3. Version Control

```bash
# Keep manifests in git
git add baseline.json
git commit -m "Add baseline snapshot"
git push
```

### 4. Automated Alerts

```bash
# Send notification on changes
if ! merklewatch verify baseline.json /data; then
    curl -X POST https://alerts.example.com/webhook \
        -d '{"text":"MerkleWatch detected changes in /data"}'
fi
```

## See Also

- [Main README](../README.md)
- [Architecture](architecture.md)
- [Ignore Rules](ignore-rules.md)
- [Manifest Format](manifest-format.md)
