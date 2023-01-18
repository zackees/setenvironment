"""
Adds setenv for unix.
"""

import os
from pathlib import Path
from typing import Union


def set_env_var(name: str, value: Union[str, Path]) -> None:
    """Sets an environment variable."""
    print("TODO implement set_env_var for macos")
    os.environ[name] = str(value)


def add_env_path(path: Union[str, Path]) -> None:
    """Adds a path to the PATH environment variable."""
    path = str(path)
    path_file = "/etc/paths"
    with open(path_file, encoding="utf-8", mode="r") as file:
        paths = file.readlines()
    if path in paths:
        return
    paths.insert(0, path)
    with open(path_file, encoding="utf-8", mode="w") as file:
        file.writelines("\n".join(paths))
