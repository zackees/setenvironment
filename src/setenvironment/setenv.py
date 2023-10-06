"""
This module provides functions for setting environment variables.
"""

# pylint: disable=import-outside-toplevel,no-else-raise,no-else-return,too-many-function-args
# flake8: noqa: E501

import os
import sys
from pathlib import Path
from typing import Optional, Union

_IS_WINDOWS = sys.platform == "win32"


def set_env_config_file(
    filepath: str = "~/.bash_aliases", ignore_error: bool = False
) -> None:
    """Sets the config file for the platform."""
    # Only works for Unix/MacOS
    if not _IS_WINDOWS:
        from .setenv_unix import set_env_config_file as unix_env_set_config_file

        unix_env_set_config_file(filepath)
        return
    if not ignore_error:
        raise NotImplementedError("set_env_config_file is not implemented for Windows.")


def set_env_var(
    var_name: str, var_value: Union[str, Path, int, float], verbose=False
) -> None:
    """Sets an environment variable for the platform."""
    var_value = str(var_value)
    if verbose:
        print(f"$$$ Setting {var_name} to {var_value}")
    if _IS_WINDOWS:
        from .setenv_win32 import set_env_var as win32_set_env_var

        var_name = str(var_name)
        var_value = str(var_value)
        win32_set_env_var(var_name, var_value)
    else:
        from .setenv_unix import set_env_var as unix_set_env_var

        var_name = str(var_name)
        var_value = str(var_value)
        unix_set_env_var(var_name, var_value)


def get_env_var(var_name: str, verbose=False) -> Optional[str]:
    """Gets an environment variable for the platform."""
    if verbose:
        print(f"$$$ Getting {var_name}")
    if _IS_WINDOWS:
        from .setenv_win32 import get_env_var as win32_get_env_var

        var_name = str(var_name)
        return win32_get_env_var(var_name)
    else:
        from .setenv_unix import get_env_var as unix_get_env_var

        var_name = str(var_name)
        return unix_get_env_var(var_name)


def get_paths() -> list[str]:
    paths = get_env_var("PATH") or ""
    return paths.split(os.path.pathsep)


def set_paths(paths: list[str]) -> None:
    sep = os.path.pathsep
    new_path_str = sep.join(paths)
    set_env_var("PATH", new_path_str)


def unset_env_var(var_name: str, verbose=False) -> None:
    """Unsets an environment variable for the platform."""
    if verbose:
        print(f"$$$ Unsetting {var_name}")
    if _IS_WINDOWS:
        from .setenv_win32 import unset_env_var as win32_unset_env_var

        var_name = str(var_name)
        win32_unset_env_var(var_name)
    else:
        from .setenv_unix import unset_env_var as unix_unset_env_var

        var_name = str(var_name)
        unix_unset_env_var(var_name)


def add_env_path(new_path: Union[Path, str]) -> None:
    """Adds a path to the front of the PATH environment variable."""
    new_path = str(new_path)
    if _IS_WINDOWS:
        from .setenv_win32 import add_env_path as win32_add_env_path

        win32_add_env_path(new_path)
    else:
        from .setenv_unix import add_env_path as unix_add_env_path

        unix_add_env_path(new_path)


def add_template_path(env_var: str, new_path: Union[Path, str]) -> None:
    """Adds a path to the front of the PATH environment variable."""
    new_path = str(new_path)
    if _IS_WINDOWS:
        from .setenv_win32 import add_template_path as win32_add_template_path

        win32_add_template_path(env_var, new_path)
    else:
        from .setenv_unix import add_template_path as unix_add_template_path

        unix_add_template_path(env_var, new_path)


def remove_template_path(env_var: str, path: Union[Path, str]) -> None:
    """Removes a path from the PATH environment variable."""
    path = str(path)
    if _IS_WINDOWS:
        from .setenv_win32 import remove_template_path as win32_remove_template_path

        win32_remove_template_path(env_var, path)
    else:
        from .setenv_unix import remove_template_path as unix_remove_template_path

        unix_remove_template_path(env_var, path)


def remove_env_path(path: Union[Path, str]) -> None:
    """Removes a path from the PATH environment variable."""
    path = str(path)
    if _IS_WINDOWS:
        from .setenv_win32 import remove_env_path as win32_remove_env_path

        win32_remove_env_path(path)
    else:
        from .setenv_unix import remove_env_path as unix_remove_env_path

        unix_remove_env_path(path)
