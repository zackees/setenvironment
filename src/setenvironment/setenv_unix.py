"""
Adds setenv for unix.
"""

# pylint: disable=fixme

import os
from pathlib import Path
from typing import Union

SOURCE_FILES = ["~/.bash_profile", "~/.bashrc", "~/.bash_login", "~/.profile"]
TARGET_FILE = None

IS_GITHUB_RUNNER = os.getenv("GITHUB_WORKFLOW")


def get_path_file() -> str:
    """Returns the file that has export PATH."""
    global TARGET_FILE  # pylint: disable=global-statement
    if TARGET_FILE is not None:
        return TARGET_FILE
    # Return the first file that has export PATH
    for file in SOURCE_FILES:
        if os.path.isfile(file):
            with open(file, encoding="utf-8", mode="r") as filed:
                for line in filed.readlines():
                    if line.startswith("export PATH="):
                        TARGET_FILE = file
                        return TARGET_FILE
    raise FileNotFoundError("No file found that has export PATH")


def set_env_var(name: str, value: Union[str, Path]) -> None:
    """Sets an environment variable."""
    value = str(value)
    os.environ[name] = value
    os.system(f"export {name}={value}")
    if IS_GITHUB_RUNNER:  # TODO: Fix
        return
    bash_profile = get_path_file()
    with open(bash_profile, encoding="utf-8", mode="r") as file:
        lines = file.readlines()
    with open(bash_profile, encoding="utf-8", mode="w") as file:
        found = False
        for line in lines:
            if line.startswith(f"export {name}="):
                file.write(f"export {name}={value}\n")
                found = True
            else:
                file.write(line)
        if not found:
            file.write(f"export {name}={value}\n")


def add_env_path(path: Union[str, Path]) -> None:
    """Adds a path to the PATH environment variable."""
    path = str(path)
    paths = os.environ["PATH"].split(":")
    if path not in paths:
        paths.insert(0, path)
        os.environ["PATH"] = ":".join(paths)
    os.system(f"export PATH={os.environ['PATH']}")
    if IS_GITHUB_RUNNER:
        return
    bash_profile = get_path_file()
    with open(bash_profile, encoding="utf-8", mode="r") as file:
        lines = file.readlines()
    with open(bash_profile, encoding="utf-8", mode="w") as file:
        found = False
        for line in lines:
            # does export path exist in this line?
            if path in line:
                found = True
            if not found and line.startswith("export PATH="):
                old_path = line.strip().split("=")[-1]
                line = f"export PATH={path}:{old_path}\n"
                found = True
            file.write(line)
        if not found:
            # Append line if not found
            old_path = os.environ["PATH"]
            file.write(f"export PATH={path}:{old_path}\n")
