# setenvironment

[![Actions Status](../../workflows/MacOS_Tests/badge.svg)](../../actions/workflows/push_macos.yml)
[![Actions Status](../../workflows/Win_Tests/badge.svg)](../../actions/workflows/push_win.yml)
[![Actions Status](../../workflows/Ubuntu_Tests/badge.svg)](../../actions/workflows/push_ubuntu.yml)

[![Linting](../../actions/workflows/lint.yml/badge.svg)](../../actions/workflows/lint.yml)

```bash
> pip install setenvironment
> setenviroment_set foo bar
> setenviroment_unset foo
> setenviroment_addpath /my/path
> setenviroment_removepath /my/path
```

```python
from setenvironment import set_env_var, add_env_path
set_env_var("FOO", "BAR")
add_env_path("MYPATH")
```

Cross platform way to set the environment.

When setting variables this tool will:
  * unix/macos
    * export the variable (so you can source the script)
    * set the os.environ to the proper value
    * write the value to the .bashrc file (make sure it's chmod +w)
  * win32
    * writes to the registery
    * broadcasts the new value (cmd.exe ignores this though) to all available processes

# Release Notes
  * 1.0.0: Initial release