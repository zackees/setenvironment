"""
Adds setenv for unix.
"""

import os


def set_env_var(name: str, value: str) -> None:
    """Sets an environment variable."""
    print("TODO implement set_env_var for macos")
    os.environ[name] = str(value)


def add_env_path(path: str) -> None:
    """Adds a path to the PATH environment variable."""
    path_file = "/etc/paths"
    with open(path_file, encoding="utf-8", mode="r") as file:
        paths = file.readlines()
    if path in paths:
        return
    paths.insert(0, path)
    with open(path_file, encoding="utf-8", mode="w") as file:
        file.writelines("\n".join(paths))
