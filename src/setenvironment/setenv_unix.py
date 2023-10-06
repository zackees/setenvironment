"""
Adds setenv for unix.
"""

import os
from typing import List, Optional

from .util import read_utf8, write_utf8


def get_target() -> str:
    """Returns the target file."""
    if os.environ.get("SETENVIRONMENT_CONFIG_FILE"):
        config_file = os.environ["SETENVIRONMENT_CONFIG_FILE"]
        return os.path.expanduser(config_file)
    # Get the dictionary attached to

    for srcs in ["~/.bash_aliases", "~/.bash_profile", "~/.bashrc"]:
        src = os.path.expanduser(srcs)
        if os.path.exists(src):
            break
    else:
        raise FileNotFoundError("Could not find any bash config file")
    return src


def set_env_config_file(filepath: str) -> None:
    """Sets the target file."""
    os.environ["SETENVIRONMENT_CONFIG_FILE"] = filepath


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


def get_env_var(name: str) -> Optional[str]:
    """Gets an environment variable."""
    filelines = read_utf8(get_target()).splitlines()
    for line in filelines:
        if line.startswith("export " + name + "="):
            return line.split("=")[1].strip()
    return None


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


# unix implementation:


def parse_paths(path_str: str) -> List[str]:
    """Parses a path string into a list of paths."""
    return path_str.split(os.path.pathsep)


def add_template_path(env_var: str, new_path: str) -> None:
    assert "$" not in env_var, "env_var should not contain $"
    assert "$" not in new_path, "new_path should not contain $"
    path_str = get_env_var("PATH")
    tmp_env_var = f"${env_var}"
    if path_str:
        paths = parse_paths(path_str)
        if tmp_env_var not in paths:
            paths.insert(0, tmp_env_var)
            new_path_str = os.path.pathsep.join(paths)
            set_env_var("PATH", new_path_str)
    else:
        add_env_path(tmp_env_var)
    env_paths = get_env_var(env_var)
    if env_paths is None:
        set_env_var(env_var, new_path)
        return
    var_paths = parse_paths(env_paths)
    if new_path not in var_paths:
        var_paths.insert(0, new_path)
        new_var_path_str = os.path.pathsep.join(var_paths)
        set_env_var(env_var, new_var_path_str)


def remove_template_path(
    env_var: str, path_to_remove: str, remove_if_empty: bool
) -> None:
    assert "$" not in env_var, "env_var should not contain $"
    assert "$" not in path_to_remove, "path_to_remove should not contain $"
    var_paths = parse_paths(get_env_var(env_var) or "")
    if path_to_remove not in var_paths:
        return
    var_paths = [path for path in var_paths if path != path_to_remove]
    new_var_path_str = os.path.pathsep.join(var_paths)
    if not new_var_path_str and remove_if_empty:
        unset_env_var(env_var)
        return
    set_env_var(env_var, new_var_path_str)
