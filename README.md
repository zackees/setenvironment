# setenvironment

[![Actions Status](../../workflows/MacOS_Tests/badge.svg)](../../actions/workflows/push_macos.yml)
[![Actions Status](../../workflows/Win_Tests/badge.svg)](../../actions/workflows/push_win.yml)
[![Actions Status](../../workflows/Ubuntu_Tests/badge.svg)](../../actions/workflows/push_ubuntu.yml)

[![Linting](../../actions/workflows/lint.yml/badge.svg)](../../actions/workflows/lint.yml)

```bash
pip install setenvironment
```

```python
from setenvironment import set_env_var, add_env_path
set_env_var("FOO", "BAR")
add_env_path("MYPATH")
```

Cross platform way to set the environment.

Note that windows does not propagate settings to open terminals as the HWND_BROADCAST, WM_SETTINGCHANGE
event is ignored.

This lib is in alpha state and MacOS/Linux is not well supported at this time.

# Release Notes
  * TODO