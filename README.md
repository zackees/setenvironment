# setenvironment

[![MacOS_Tests](https://github.com/zackees/setenvironment/actions/workflows/push_macos.yml/badge.svg)](https://github.com/zackees/setenvironment/actions/workflows/push_macos.yml)
[![Win_Tests](https://github.com/zackees/setenvironment/actions/workflows/push_win.yml/badge.svg)](https://github.com/zackees/setenvironment/actions/workflows/push_win.yml)
[![Ubuntu_Tests](https://github.com/zackees/setenvironment/actions/workflows/push_ubuntu.yml/badge.svg)](https://github.com/zackees/setenvironment/actions/workflows/push_ubuntu.yml)

[![Linting](https://github.com/zackees/setenvironment/actions/workflows/lint.yml/badge.svg)](https://github.com/zackees/setenvironment/actions/workflows/lint.yml)

Finally, a cross platform way to set system environment variables and paths that are persistant across reboots.

Works with Windows, MacOS and Linux and github runners, see note below.

Extensively tested.

## Command line interface

```bash
# Setting environmental variables
setenvironment show
setenviornment bashrc  # unix only.
setenvironment set foo bar
setenvironment has foo
setenvironment get foo
setenvironment del foo
# Path manipulation.
setenvironment addpath /my/path
setenvironment get PATH
setenvironment delpath /my/path
setenvironment refresh "echo this command is in a refreshed environment"
```

## Python API

```python
from setenvironment import (
    set_env_var, add_env_path, unset_env_var, remove_env_path, set_config_file, reload_environment, ...
)
# by default, ~/.bashrc is used
set_env_var("FOO", "BAR")
get_env_var("FOO") # returns BAR
add_env_path("MYPATH")
unset_env_var("FOO")
remove_env_path("MYPATH")
# use ~/.bash_profile instead (no op on Windows)
set_config_file("~/.bash_profile")
set_env_var("FOO", "BAR")
add_env_path("MYPATH")
unset_env_var("FOO")
remove_env_path("MYPATH")
# Loads settings into the current environment. This reads the
# registry on windows or the ~/.bashrc file on unix.
reload_environment()
# Path groups are usefull for uninstall programs. Each add
# copies the path both into the PATH and also to the key.
# When you want to remove paths you can query the key and selectively
# remove paths that are in the set.
add_to_path_group("MYPATHKEY", "/path/to/dir")
remove_to_path_group("MYPATHKEY", "/path/to/dir")
# Or else you can just remove ALL of the paths at once.
remove_path_group("MYPATHKEY")
```


## Github

These are designed to be compatible with github runners.

Ubuntu MUST use the following to make this package work.

```
name: Ubuntu_Tests

# Directs GitHub to run tests using ~/.bashrc
defaults:
    run:
      shell: bash -ieo pipefail {0}

on: [push]
```

## Windows

Paths are set in the registery and the current os.environ

  * writes to the registery
  * broadcasts the new value (cmd.exe ignores this though) to all available processes
  * paths like `/my/path` will be converted to `\\my\\path`

## MacOS / Linux

Paths are set in either `~/.bash_aliases` or `~/.bash_profile` or `~/.bashrc` file or you can override it, see `set_config_file(...)` and the command line arguments if using the command line api.

  * export the variable (so you can source the script)
  * set the os.environ to the proper value
  * write the value to the .bashrc file (make sure it's chmod +w)


# Release Notes
  * 2.0.3: Disables the refresh.cmd, since it doesn't work for subprocesses.
  * 2.0.2: Re-enabled broadcast changes on win32, fixing new terminal launch.
  * 2.0.1: Bug fix.
  * 2.0.0: Rewrite. New command line api. Extensively tested on mac/win/ubuntu X github.
