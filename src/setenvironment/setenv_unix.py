"""
Adds setenv for unix.
"""

import os
from functools import cache

from .util import read_utf8, write_utf8


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
    export_cmd = f"export {name}={value}"
    for i, line in enumerate(lines):
        if line.startswith("export " + name + "="):
            lines[i] = export_cmd
            os.system(export_cmd)
            found = True
            break
    if not found:
        lines.append(export_cmd)
        os.system(export_cmd)
    new_file = "\n".join(lines)
    if new_file != orig_file:
        write_utf8(settings_file, new_file)


def unset_env_var(name: str) -> None:
    """Unsets an environment variable."""
    if name in os.environ:
        del os.environ[name]
    settings_file = get_target()
    orig_file = read_utf8(settings_file)
    lines = orig_file.splitlines()
    found = False
    for i, line in enumerate(lines):
        if line.startswith("export " + name + "="):
            lines[i] = None  # type: ignore
            found = True
            break
    if found:
        lines = [line for line in lines if line is not None]
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
        export_cmd = f"export PATH=$PATH:{path}"
        os.system(export_cmd)
        lines.append(export_cmd)
    new_file = "\n".join(lines)
    if new_file != orig_file:
        write_utf8(settings_file, new_file)


def remove_env_path(path: str) -> None:
    """Removes a path from the PATH environment variable."""
    # remove path from os.environ['PATH'] if it does not exist
    path_list = os.environ["PATH"].split(os.pathsep)
    if path in path_list:
        path_list.remove(path)
        os.environ["PATH"] = os.pathsep.join(path_list)
    settings_file = get_target()
    orig_file = read_utf8(settings_file)
    lines = orig_file.splitlines()
    found = False
    for i, line in enumerate(lines):
        if line.startswith("export PATH=") and path in line:
            lines[i] = None  # type: ignore
            found = True
            break
    if found:
        lines = [line for line in lines if line is not None]
        new_file = "\n".join(lines)
        if new_file != orig_file:
            write_utf8(settings_file, new_file)
