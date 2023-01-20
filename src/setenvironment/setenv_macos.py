"""
Adds setenv for unix.
"""

import os
from functools import cache


def read_utf8(path: str) -> str:
    """Reads a file as utf-8."""
    with open(path, encoding="utf-8", mode="r") as file:
        return file.read()


def write_utf8(path: str, text: str) -> None:
    """Writes a file as utf-8."""
    with open(path, encoding="utf-8", mode="w") as file:
        file.write(text)


@cache
def get_target() -> str:
    """Returns the target file."""
    # Get the dictionary attached to
    bashrc = os.path.expanduser("~/.bashrc")
    if ".bash_profile" not in read_utf8(bashrc):
        return bashrc
    return os.path.expanduser("~/.bash_profile")


def set_env_var(name: str, value: str) -> None:
    """Sets an environment variable."""
    os.environ[name] = str(value)
    settings_file = get_target()
    orig_file = read_utf8(settings_file)
    lines = orig_file.splitlines()
    found = False
    for i, line in enumerate(lines):
        if line.startswith("export " + name + "="):
            lines[i] = f"export {name}={value}"
            found = True
            break
    if not found:
        lines.append(f"export {name}={value}")
    new_file = "\n".join(lines)
    if new_file != orig_file:
        write_utf8(settings_file, new_file)


def add_env_path(path: str) -> None:
    """Adds a path to the PATH environment variable."""
    # add path to os.environ['PATH'] if it does not exist
    path_list = os.environ["PATH"].split(os.path.sep)
    if path not in path_list:
        os.environ["PATH"] = path + os.pathsep + os.environ["PATH"]
    settings_file = get_target()
    orig_file = read_utf8(settings_file)
    lines = orig_file.splitlines()
    found = False
    for line in lines:
        if line.startswith("export PATH=") and path in line:
            found = True
            break
    if not found:
        lines.append(f"export PATH=$PATH:{path}")
    new_file = "\n".join(lines)
    if new_file != orig_file:
        write_utf8(settings_file, new_file)
