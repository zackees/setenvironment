# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`setenvironment` is a cross-platform Python package for setting system environment variables and PATH entries that persist across reboots. It works on Windows, MacOS, and Linux.

## Key Commands

### Testing
```bash
# Run all tests
./test.sh

# Or directly with unittest
cd tests && python -m unittest discover

# Using tox (Python 3.10)
tox
```

### Linting
```bash
# Run all linters and formatters
./lint.sh

# Individual tools (run from project root)
ruff --fix src tests
isort src tests
black src tests
flake8 src tests
mypy src tests
```

### Building and Publishing
```bash
# Build the package
python -m build

# Upload to PyPI (requires credentials)
./upload_package.sh
```

## Architecture

### Platform Abstraction Pattern

The codebase uses a consistent platform abstraction pattern where `setenv.py` provides a unified API that delegates to platform-specific implementations:

- **Main API** (`src/setenvironment/setenv.py`): Platform-agnostic functions that check `sys.platform` and import the appropriate implementation
- **Windows** (`src/setenvironment/setenv_win32.py`): Uses Windows Registry via `win32api` (pywin32)
- **Unix** (`src/setenvironment/setenv_unix.py`): Uses bash configuration files (`~/.bashrc`, `~/.bash_profile`, or `~/.bash_aliases`)

### Core Components

1. **Registry Layer** (`src/setenvironment/win/registry.py`): Direct Windows Registry manipulation for persisting environment variables
2. **Bash Parser** (`src/setenvironment/bash_parser.py`): Reads/writes bash configuration files on Unix systems
3. **Environment Types** (`src/setenvironment/types.py`): Data structures for representing environment state (`Environment`, `BashEnvironment`, `RegistryEnvironment`, `OsEnvironment`)
4. **OS Environment** (`src/setenvironment/os_env.py`, `src/setenvironment/os_env_json.py`): Utilities for querying current OS environment state

### Path Groups Feature

The package includes a "path groups" feature for managing sets of related paths (useful for uninstallation). Functions like `add_to_path_group()`, `remove_from_path_group()`, and `remove_path_group()` allow grouping paths under a key for batch operations.

### Windows-Specific Behavior

- Writes to User environment variables in Registry (HKEY_CURRENT_USER)
- Broadcasts WM_SETTINGCHANGE messages to notify running applications
- Automatically converts forward slashes to backslashes
- Registry changes persist immediately and affect new processes

### Unix-Specific Behavior

- By default writes to `~/.bash_aliases`, falls back to `~/.bashrc` or `~/.bash_profile`
- Config file can be overridden with `set_config_file()` or `--config` CLI flag
- Uses `export` statements for persistence
- Changes require sourcing the config file or starting a new shell

## CLI Interface

The main CLI (`src/setenvironment/main.py`) provides a unified command interface:

```bash
setenvironment set KEY VALUE
setenvironment get KEY
setenvironment del KEY
setenvironment addpath /path/to/add
setenvironment delpath /path/to/remove
setenvironment has KEY
setenvironment show         # Show current environment state
setenvironment bashrc       # Unix only: show bashrc contents
setenvironment refresh [CMD] # Reload environment and optionally run command
```

## Testing Notes

- Tests are organized by feature (e.g., `test_setenv.py`, `test_setpath.py`, `test_path_group.py`)
- Platform-specific tests: `test_win.py`, `test_unix.py`
- Base test class at `src/setenvironment/testing/basetest.py` provides common fixtures
- Tests extensively verify persistence and cross-session behavior
