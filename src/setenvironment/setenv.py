"""
This module provides functions for setting environment variables.
"""

# pylint: disable=import-outside-toplevel,no-else-raise,no-else-return,too-many-function-args
# flake8: noqa: E501
# pylint: disable=C0116

import os
import sys
from pathlib import Path
from typing import Optional, Union

from setenvironment.types import Environment

_IS_WINDOWS = sys.platform == "win32"


def set_env_var(
    var_name: str,
    var_value: Union[str, Path, int, float],
    verbose=False,
    update_curr_environment: bool = True,
) -> None:
    """Sets an environment variable for the platform."""
    var_value = str(var_value)
    if verbose:
        print(f"$$$ Setting {var_name} to {var_value}")
    if _IS_WINDOWS:
        from .setenv_win32 import set_env_var as win32_set_env_var

        var_name = str(var_name)
        var_value = str(var_value)
        win32_set_env_var(
            var_name, var_value, update_curr_environment=update_curr_environment
        )
    else:
        from .setenv_unix import set_env_var as unix_set_env_var

        var_name = str(var_name)
        var_value = str(var_value)
        unix_set_env_var(
            var_name, var_value, update_curr_environment=update_curr_environment
        )


def get_env_var(var_name: str, verbose=False, resolve=None) -> Optional[str]:
    """Gets an environment variable for the platform."""
    if verbose:
        print(f"$$$ Getting {var_name}")
    if _IS_WINDOWS:
        from .setenv_win32 import get_env_var as win32_get_env_var

        var_name = str(var_name)
        return win32_get_env_var(var_name, resolve=resolve)
    else:
        from .bash_parser import bash_read_variable

        var_name = str(var_name)
        return bash_read_variable(var_name)


def get_paths(resolve=None) -> list[str]:
    if resolve is None:
        resolve = True if _IS_WINDOWS else False
    paths = get_env_var("PATH", resolve=resolve) or ""
    path_list = paths.split(os.path.pathsep)
    resolved_paths = []
    for path in path_list:
        if "$path" == path.lower():
            continue
        if resolve:
            inner_resolved_paths = os.path.expandvars(path).split(os.path.pathsep)
            resolved_paths.extend(inner_resolved_paths)
        else:
            resolved_paths.append(path)
    resolved_paths = [p for p in resolved_paths if p]
    return resolved_paths


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


def remove_env_path(path: Union[Path, str]) -> None:
    """Removes a path from the PATH environment variable."""
    path = str(path)
    if _IS_WINDOWS:
        from .setenv_win32 import remove_env_path as win32_remove_env_path

        win32_remove_env_path(path)
    else:
        from .setenv_unix import remove_env_path as unix_remove_env_path

        unix_remove_env_path(path)


def reload_environment(verbose=False, resolve=False) -> None:
    """Reloads the environment."""
    if _IS_WINDOWS:
        from .setenv_win32 import reload_environment as win32_reload_environment

        # Note that windows always resolves the paths.
        win32_reload_environment(verbose=verbose)
    else:
        from .setenv_unix import reload_environment as unix_reload_environment

        unix_reload_environment(verbose=verbose, resolve=resolve)


def get_env() -> Environment:
    """Gets the environment."""
    if _IS_WINDOWS:
        from .setenv_win32 import get_env as win32_get_env

        return win32_get_env()
    else:
        from .setenv_unix import get_env as unix_get_env

        return unix_get_env()


def add_to_path_group(group_name: str, new_path: str) -> None:
    """Adds a path to the front of the PATH environment variable."""
    if _IS_WINDOWS:
        from .setenv_win32 import add_path_group as win32_add_path_group

        win32_add_path_group(group_name, new_path)
    else:
        from .setenv_unix import add_path_group as unix_add_path_group

        unix_add_path_group(group_name, new_path)


def remove_from_path_group(group_name: str, path_to_remove: str) -> None:
    """Removes a path from the PATH environment variable."""
    if _IS_WINDOWS:
        from .setenv_win32 import remove_from_path_group as win32_remove_path_group

        win32_remove_path_group(group_name, path_to_remove)
    else:
        from .setenv_unix import remove_from_path_group as unix_remove_path_group

        unix_remove_path_group(group_name, path_to_remove)


# remove_path_group
def remove_path_group(group_name: str) -> None:
    """Removes a path from the PATH environment variable."""
    if _IS_WINDOWS:
        from .setenv_win32 import remove_path_group as win32_remove_path_group

        win32_remove_path_group(group_name)
    else:
        from .setenv_unix import remove_path_group as unix_remove_path_group

        unix_remove_path_group(group_name)
