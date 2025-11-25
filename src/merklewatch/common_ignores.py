
# Common ignore patterns grouped by category
COMMON_IGNORES = {
    "Operating System": [
        ".DS_Store",
        "Thumbs.db",
        "desktop.ini",
        "Icon?",
        "ehthumbs.db"
    ],
    "Editors & IDEs": [
        ".vscode/",
        ".idea/",
        "*.sublime-project",
        "*.sublime-workspace",
        "*~",
        ".#*",
        "*.swp",
        "*.swo",
        "Session.vim",
        ".metadata/"
    ],
    "Python": [
        "__pycache__/",
        "*.py[cod]",
        "*$py.class",
        "*.pyo",
        "*.pyd",
        "venv/",
        "env/",
        ".venv/",
        "pip-wheel-metadata/",
        "*.egg-info/",
        ".eggs/"
    ],
    "Node.js": [
        "node_modules/",
        "npm-debug.log*",
        "yarn-debug.log*",
        "yarn-error.log*",
        "pnpm-debug.log*",
        "package-lock.json",
        "yarn.lock",
        "pnpm-lock.yaml"
    ],
    "Java / JVM": [
        "*.class",
        "*.jar",
        "*.war",
        "*.ear",
        "target/",
        "build/",
        "*.iml"
    ],
    "Rust / Cargo": [
        "target/",
        "**/*.rlib",
        "Cargo.lock"
    ],
    "Go": [
        "bin/",
        "*.exe",
        "*.test"
    ],
    ".NET": [
        "bin/",
        "obj/",
        "*.user",
        "*.suo",
        "*.cache"
    ],
    "C/C++": [
        "*.o",
        "*.obj",
        "*.so",
        "*.exe",
        "build/"
    ],
    "Build, Packaging & CI": [
        "dist/",
        "build/",
        "out/",
        "coverage/",
        ".coverage",
        "coverage.xml",
        "htmlcov/",
        ".pytest_cache/",
        ".tox/",
        ".nox/",
        "/.cache",
        "pip-wheel-metadata/"
    ],
    "Container / Docker": [
        "docker-compose.override.yml",
        "Dockerfile.*.local",
        "*.dockerfile"
    ],
    "Archives, Backups & Large Files": [
        "*.zip",
        "*.tar",
        "*.tar.gz",
        "*.tgz",
        "*.rar",
        "*.7z",
        "*.gz",
        "*.bak",
        "*.old",
        "*.backup"
    ],
    "Logs & Temp": [
        "*.log",
        "logs/",
        "*.tmp",
        "*.temp",
        "tmp/"
    ],
    "Git": [
        ".git/",
        ".gitignore"
    ]
}

def get_all_common_patterns():
    """Return a flat list of all common patterns."""
    all_patterns = []
    for category, patterns in COMMON_IGNORES.items():
        all_patterns.extend(patterns)
    return sorted(list(set(all_patterns)))
