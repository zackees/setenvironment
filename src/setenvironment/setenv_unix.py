"""
Adds setenv for unix.
"""

# pylint: disable=C0116
# flake8: noqa: E501

import os
import re
import warnings
from typing import List, Optional

from .types import Environment
from .util import read_utf8, write_utf8

START_MARKER = "# START setenvironment"
END_MARKER = "# END setenvironment"


def read_bash_file_lines(filepath: str | None = None) -> list[str]:
    """Reads a bash file."""
    filepath = filepath or get_target()
    with open(filepath, encoding="utf8", mode="r") as file:
        lines = file.read().splitlines()
    # read all lines from START_MARKER to END_MARKER
    start_index = -1
    end_index = -1
    for i, line in enumerate(lines):
        if line.startswith(START_MARKER):
            start_index = i + 1
        if line.startswith(END_MARKER):
            end_index = i
    if start_index == -1:
        return []
    if end_index == -1:
        warnings.warn(f"Could not find {END_MARKER} in {filepath}")
        return lines[start_index:]
    return lines[start_index:end_index]


def set_bash_file_lines(lines: list[str], filepath: str | None = None) -> None:
    """Adds new lines to the start of the bash file in the START_MARKER to END_MARKER section."""
    filepath = filepath or get_target()
    file_read = read_utf8(filepath)
    if START_MARKER not in file_read:
        file_read += "\n" + START_MARKER + "\n" + END_MARKER + "\n"
        write_utf8(filepath, file_read)
        file_read = read_utf8(filepath)  # read again
    orig_lines = file_read.splitlines()
    # read all lines from START_MARKER to END_MARKER
    outlines = []
    found_start_marker = False
    found_end_marker = False
    for line in orig_lines:
        if line.startswith(START_MARKER):
            outlines.append(line)
            found_start_marker = True
            outlines.extend(lines)
            continue
        if line.startswith(END_MARKER):
            found_end_marker = True
            outlines.append(line)
            continue
        if not found_start_marker or found_end_marker:
            outlines.append(line)
            continue
    write_utf8(filepath, "\n".join(outlines))


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


def set_env_var(name: str, value: str, update_curr_environment=True) -> None:
    """Sets an environment variable."""
    if update_curr_environment:
        os.environ[name] = str(value)
    settings_files = get_target()
    lines = read_bash_file_lines(settings_files)
    found = False
    export_cmd = f"export {name}={value}"
    for i, line in enumerate(lines):
        if line.startswith("export " + name + "="):
            lines[i] = export_cmd
            found = True
            break
    if not found:
        lines.append(export_cmd)
    if update_curr_environment:
        os.system(export_cmd)
    set_bash_file_lines(lines, settings_files)


def get_all_env_vars() -> dict[str, str]:
    """Gets all environment variables."""
    settings_file = get_target()
    lines = read_bash_file_lines(settings_file)
    env_vars: dict[str, str] = {}
    for line in lines:
        if line.startswith("export "):
            name, value = line[7:].split("=", 1)
            env_vars[name] = value
    return env_vars


def get_env_var(name: str) -> Optional[str]:
    """Gets an environment variable."""
    settings_file = get_target()
    lines = read_bash_file_lines(settings_file)
    for line in lines:
        if line.startswith("export " + name + "="):
            return line[7:].split("=")[1].strip()
    return None


def unset_env_var(name: str) -> None:
    """Unsets an environment variable."""
    if name in os.environ:
        del os.environ[name]
    settings_file = get_target()
    lines = read_bash_file_lines(settings_file)
    found = False
    for i, line in enumerate(lines):
        if line.startswith("export " + name + "="):
            lines[i] = None  # type: ignore
            found = True
            break
    if found:
        lines = [line for line in lines if line is not None]
        set_bash_file_lines(lines, settings_file)


def add_env_path(
    path: str, verbose: bool = False, update_curr_environment: bool = True
) -> None:
    """Adds a path to the PATH environment variable."""
    path_list = os.environ["PATH"].split(os.path.sep)
    if path not in path_list and update_curr_environment:
        os.environ["PATH"] = path + os.pathsep + os.environ["PATH"]
    settings_file = get_target()
    lines = read_bash_file_lines(settings_file)
    found = False
    for line in lines:
        if line.startswith("export PATH=") and path in line:
            found = True
            break
    if not found:
        export_cmd = f"export PATH={path}:$PATH"
        if update_curr_environment:
            os.system(export_cmd)
        lines.append(export_cmd)
        set_bash_file_lines(lines, settings_file)


def remove_env_path(path: str, update_curr_environment=True) -> None:
    """Removes a path from the PATH environment variable."""
    # remove path from os.environ['PATH'] if it does not exist
    if update_curr_environment:
        path_list = os.environ["PATH"].split(os.pathsep)
        if path in path_list:
            path_list.remove(path)
            os.environ["PATH"] = os.pathsep.join(path_list)
    settings_file = get_target()
    lines = read_bash_file_lines(settings_file)
    found = False
    for i, line in enumerate(lines):
        if line.startswith("export PATH=") and path in line:
            lines[i] = None  # type: ignore
            found = True
            break
    if found:
        lines = [line for line in lines if line is not None]
        set_bash_file_lines(lines, settings_file)


def parse_paths(path_str: str) -> List[str]:
    """Parses a path string into a list of paths."""
    path_str = path_str.strip()
    if not path_str:
        return []
    return path_str.split(os.path.pathsep)


def add_template_path(
    env_var: str, new_path: str, update_curr_environment=True
) -> None:
    assert "$" not in env_var, "env_var should not contain $"
    assert "$" not in new_path, "new_path should not contain $"
    path_str = get_env_var("PATH")
    tmp_env_var = f"${env_var}"
    if path_str:
        paths = parse_paths(path_str)
        if tmp_env_var not in paths:
            paths.insert(0, tmp_env_var)
            new_path_str = os.path.pathsep.join(paths)
            set_env_var(
                "PATH",
                new_path_str,
                update_curr_environment=update_curr_environment,
            )
    else:
        add_env_path(tmp_env_var, update_curr_environment=update_curr_environment)
    env_paths = get_env_var(env_var)
    if env_paths is None:
        set_env_var(env_var, new_path, update_curr_environment=update_curr_environment)
        return
    var_paths = parse_paths(env_paths)
    if new_path not in var_paths:
        var_paths.insert(0, new_path)
        new_var_path_str = os.path.pathsep.join(var_paths)
        set_env_var(
            env_var,
            new_var_path_str,
            update_curr_environment=update_curr_environment,
        )


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
        paths = parse_paths(get_env_var("PATH") or "")
        if f"${env_var}" in paths:
            paths = [path for path in paths if path != f"${env_var}"]
            new_path_str = os.path.pathsep.join(paths)
            set_env_var("PATH", new_path_str)
        return
    set_env_var(env_var, new_var_path_str)


def path_resolver(path: str) -> str:
    """Resolves a path that contains Unix environment variables."""
    # The regex pattern to search for $VAR_NAME patterns
    pattern = re.compile(r"\$([a-zA-Z_][a-zA-Z0-9_]*)")

    def replace_env_var(match):
        """Replace matched environment variable with its value."""
        var_name = match.group(1)  # Extract the VAR_NAME from the match
        out = os.environ.get(
            var_name, match.group(0)
        )  # Return environment variable value or the original string if not found
        return out

    return pattern.sub(replace_env_var, path)


def reload_environment(verbose: bool) -> None:
    """Reloads the environment."""
    # This is nearly the same as win version. Please keep them in same.
    env: Environment = get_env()
    path_list = env.paths
    env_vars = env.vars
    for key, val in env_vars.items():
        if key == "PATH":
            continue
        resolved_path = path_resolver(val)
        if resolved_path is None:
            warnings.warn(f"Could not resolve path {val}")
            continue
        if verbose:
            print(f"Setting {key} to {resolved_path}")
        os.environ[key] = val
    path_list = [path_resolver(path) for path in path_list]
    path_list_str = os.path.pathsep.join(path_list)
    os.environ["PATH"] = path_list_str
    if verbose:
        print(f"Setting PATH to {path_list_str}")


def get_env() -> Environment:
    """Returns the environment."""
    env_vars = get_all_env_vars()
    paths = parse_paths(env_vars.get("PATH", ""))
    return Environment(
        vars=env_vars,
        paths=paths,
    )
