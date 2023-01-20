"""
This module provides functions for setting environment variables.
"""

# pylint: disable=import-outside-toplevel

import sys
from pathlib import Path
from typing import Union


def set_env_var(var_name: str, var_value: Union[str, Path, int, float], verbose=False):
    """Sets an environment variable for the platform."""
    var_value = str(var_value)
    if verbose:
        print(f"$$$ Setting {var_name} to {var_value}")
    if sys.platform == "win32":
        from .setenv_win32 import set_env_var as win32_set_env_var

        var_name = str(var_name)
        var_value = str(var_value)
        win32_set_env_var(var_name, var_value)
    else:
        from .setenv_unix import set_env_var as unix_set_env_var

        var_name = str(var_name)
        var_value = str(var_value)
        unix_set_env_var(var_name, var_value)


def add_env_path(new_path: Union[Path, str]):
    """Adds a path to the front of the PATH environment variable."""
    new_path = str(new_path)
    if sys.platform == "win32":
        from .setenv_win32 import add_env_path as win32_add_env_path

        win32_add_env_path(new_path)
    else:
        from .setenv_unix import add_env_path as unix_add_env_path

        unix_add_env_path(new_path)
