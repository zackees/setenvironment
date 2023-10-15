# setenvironment

[![MacOS_Tests](https://github.com/zackees/setenvironment/actions/workflows/push_macos.yml/badge.svg)](https://github.com/zackees/setenvironment/actions/workflows/push_macos.yml)
[![Win_Tests](https://github.com/zackees/setenvironment/actions/workflows/push_win.yml/badge.svg)](https://github.com/zackees/setenvironment/actions/workflows/push_win.yml)
[![Ubuntu_Tests](https://github.com/zackees/setenvironment/actions/workflows/push_ubuntu.yml/badge.svg)](https://github.com/zackees/setenvironment/actions/workflows/push_ubuntu.yml)

[![Linting](https://github.com/zackees/setenvironment/actions/workflows/lint.yml/badge.svg)](https://github.com/zackees/setenvironment/actions/workflows/lint.yml)

Finally, a cross platform way to set system environment variables and paths that are persistant across reboots.

Works with Windows, MacOS and Linux.

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

## Command line interface

```bash
# Setting environmental variables
setenvironment set foo bar
setenvironment remove foo
# Adding and removing paths.
setenvironment addpath /my/path
setenvironment removepath /my/path
```

## Github

These are designed to be compatible with github runners.

However, ubuntu runners don't have a ~/.bashrc file
that is sourced by default. However adding this to your
runner file will turn it on

```
name: Ubuntu_Tests

# Directs GitHub to run tests using ~/.bashrc
defaults:
    run:
      shell: bash -ieo pipefail {0}

on: [push]
```

## Command Line API

```bash
> pip install setenvironment
> setenviroment_set foo bar
> setenvironment_get foo
> setenviroment_unset foo
> setenviroment_addpath /my/path
> setenviroment_removepath /my/path
# or use custom config file
> setenvironment_set foo bar --config-file ~/.bash_profile
# or set using an environment setting
> export SETENVIRONMENT_CONFIG_FILE = ~/.bash_profile
> setenviroment_set foo bar
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

## Github runnier - linux

To force the ubuntu runner to use the ~/bashrc file, use the following:

```
name: Ubuntu_Fullinstall
on: [push]
defaults:
    run:
      shell: bash -ieo pipefail {0}
```

# Release Notes
  * 1.2.0: Win32 now resolves paths with variables in it since this wasn't being done before.
  * 1.1.10: `reload_environment()` improvements on full environment reloading.
  * 1.1.9: Adds `remove_template_group`
  * 1.1.8: Updated finding the bashrc file to better support github runners that use ~/.profile.
  * 1.1.6: Improved `reload_environment()` to preserve existing os paths.
  * 1.1.5: Fixes unix paths where the path would be appended instead of prepended.
  * 1.1.4: `reload_environment()` now supports template substitution.
  * 1.1.3: Unix/Macos: bashrc now uses a START / END markers to contain environment settings.
  * 1.1.1: Adds `add_template_path` and `remove_template_path`
  * 1.1.0: stashes settings in ~/.bash_aliases, ~/.bash_profile, ~/.bashrc
  * 1.0.10: Win32: path is now set in the user environment instead of the system environment (removes the need for admin rights)
  * 1.0.9: Win32: Improve expansion of keys, remove duplicates found in os.environ['PATH']
  * 1.0.8: Adds fix for windows expansion of keys
  * 1.0.7: Adds get_env_var
  * 1.0.6: Fixes readme
  * 1.0.3: Fix relative links in badges to be absolute when uploaded to pypi
  * 1.0.2: Fix badges on pypi
  * 1.0.1: Adds setenvironment_get
  * 1.0.0: Initial release
