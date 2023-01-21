# setenvironment

[![Actions Status](../../workflows/MacOS_Tests/badge.svg)](../../actions/workflows/push_macos.yml)
[![Actions Status](../../workflows/Win_Tests/badge.svg)](../../actions/workflows/push_win.yml)
[![Actions Status](../../workflows/Ubuntu_Tests/badge.svg)](../../actions/workflows/push_ubuntu.yml)

[![Linting](../../actions/workflows/lint.yml/badge.svg)](../../actions/workflows/lint.yml)

Cross platform way to set system environment variables and paths that are persistant across reboots.

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

```python
from setenvironment import set_env_var, add_env_path, unset_env_var, remove_env_path, set_config_file
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
```


When setting variables this tool will:
  * unix/macos
    * export the variable (so you can source the script)
    * set the os.environ to the proper value
    * write the value to the .bashrc file (make sure it's chmod +w)
  * win32
    * writes to the registery
    * broadcasts the new value (cmd.exe ignores this though) to all available processes
    * paths like `/my/path` will be converted to `\\my\\path`

# Release Notes
  * 1.0.5: Another attempt to fix readme
  * 1.0.4: Another attempt to fix readme
  * 1.0.3: Fix relative links in badges to be absolute when uploaded to pypi
  * 1.0.2: Fix badges on pypi
  * 1.0.1: Adds setenvironment_get
  * 1.0.0: Initial release