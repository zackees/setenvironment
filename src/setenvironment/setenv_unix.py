"""
Adds setenv for unix.
"""

# pylint: disable=C0116
# flake8: noqa: E501

import json
import os
import subprocess
import sys

from setenvironment.bash_parser import (
    bash_append_lines,
    bash_rc_file,
    bash_read_lines,
    bash_read_variable,
    bash_write_lines,
    read_bash_file_lines,
    set_bash_file_lines,
)
from setenvironment.types import Environment
from setenvironment.util import parse_paths, remove_adjascent_duplicates


def set_env_var(name: str, value: str, update_curr_environment=True) -> None:
    """Sets an environment variable."""
    if update_curr_environment:
        os.environ[name] = str(value)
    settings_files = bash_rc_file()
    lines = read_bash_file_lines(settings_files)
    found = False
    export_cmd = f"export {name}={value}"
    for i, line in enumerate(lines):
        if line.startswith("export " + name + "="):
            lines[i] = export_cmd
            found = True
            break
    if not found:
        if name == "PATH":
            lines.append(export_cmd)
        else:
            lines.insert(0, export_cmd)
    if update_curr_environment:
        os.system(export_cmd)
    set_bash_file_lines(lines, settings_files)


def get_env_vars_from_shell(settings_file: str | None = None) -> Environment:
    # Source the provided bashrc_file, ~/.bashrc, and ~/.profile, then execute the command.
    delim = "-------- BEGIN setenviorment.os_env_json --------"
    settings_file = settings_file or bash_rc_file()
    python_exe = sys.executable
    cmd = (
        f"source ~/.profile; "
        f"source {settings_file}; "
        f"echo {delim};"
        f"{python_exe} -m setenvironment.os_env_json"
    )
    completed_process = subprocess.run(
        ["/bin/bash", "-c", cmd],
        capture_output=True,
        universal_newlines=True,
        check=True,
    )
    json_str = completed_process.stdout.split(delim)[1].strip()
    json_data = json.loads(json_str)
    paths = json_data["PATH"]
    # remove adjascent duplicates
    paths = remove_adjascent_duplicates(paths)
    out = Environment(
        vars=json_data["ENVIRONMENT"],
        paths=paths,
    )
    return out


def get_all_env_vars() -> Environment:
    """Gets all environment variables."""
    settings_file = bash_rc_file()
    shell_env: Environment = get_env_vars_from_shell(settings_file)
    return shell_env


def unset_env_var(name: str) -> None:
    """Unsets an environment variable."""
    if name in os.environ:
        del os.environ[name]
    lines = bash_read_lines()
    found = False
    for i, line in enumerate(lines):
        if line.startswith("export " + name + "="):
            lines[i] = None  # type: ignore
            found = True
            break
    if found:
        lines = [line for line in lines if line is not None]
        bash_write_lines(lines)


def add_env_path(
    path: str, verbose: bool = False, update_curr_environment: bool = True
) -> None:
    """Adds a path to the PATH environment variable."""
    if update_curr_environment:
        os.environ["PATH"] = path + os.pathsep + os.environ["PATH"]
    export_cmd = f"export PATH={path}:$PATH"
    bash_append_lines([export_cmd])
    if update_curr_environment:
        os.system(export_cmd)


def remove_env_path(path: str, update_curr_environment=True) -> None:
    """Removes a path from the PATH environment variable."""
    # remove path from os.environ['PATH'] if it does not exist
    if update_curr_environment:
        path_list = os.environ["PATH"].split(os.pathsep)
        if path in path_list:
            path_list.remove(path)
            os.environ["PATH"] = os.pathsep.join(path_list)
    settings_file = bash_rc_file()
    lines = read_bash_file_lines(settings_file)
    found = False
    for i, line in enumerate(lines):
        if line.startswith("export PATH=") and path in line:
            path_pieces = line.split(os.pathsep)
            path_pieces.remove(path)
            new_path = os.pathsep.join(path_pieces)
            lines[i] = f"export PATH={new_path}"
            found = True
    if found:
        bash_write_lines(lines)


def add_template_path(
    env_var: str, new_path: str, update_curr_environment=True
) -> None:
    assert "$" not in env_var, "env_var should not contain $"
    assert "$" not in new_path, "new_path should not contain $"
    path_str = bash_read_variable("PATH")
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
    env_paths = bash_read_variable(env_var)
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
    var_paths = parse_paths(bash_read_variable(env_var) or "")
    if path_to_remove not in var_paths:
        return
    var_paths = [path for path in var_paths if path != path_to_remove]
    new_var_path_str = os.path.pathsep.join(var_paths)
    if not new_var_path_str and remove_if_empty:
        unset_env_var(env_var)
        paths = parse_paths(bash_read_variable("PATH") or "")
        if f"${env_var}" in paths:
            paths = [path for path in paths if path != f"${env_var}"]
            new_path_str = os.path.pathsep.join(paths)
            set_env_var("PATH", new_path_str)
        return
    set_env_var(env_var, new_var_path_str)


def remove_template_group(env_var: str) -> None:
    assert "$" not in env_var, "env_var should not contain $"
    var_paths = parse_paths(bash_read_variable(env_var) or "")
    if not var_paths:
        return
    unset_env_var(env_var)
    paths = parse_paths(bash_read_variable("PATH") or "")
    if f"${env_var}" in paths:
        paths = [path for path in paths if path != f"${env_var}"]
        new_path_str = os.path.pathsep.join(paths)
        set_env_var("PATH", new_path_str)
    if not var_paths:
        return
    for path in var_paths:
        remove_template_path(env_var, path, remove_if_empty=True)
    system_var = f"${env_var}"
    paths = parse_paths(bash_read_variable("PATH") or "")
    if system_var in paths:
        paths = [path for path in paths if path != system_var]
        new_path_str = os.path.pathsep.join(paths)
        set_env_var("PATH", new_path_str)
        os.environ["PATH"] = new_path_str


def reload_environment(verbose: bool, resolve: bool) -> None:
    """Reloads the environment."""
    # This is nearly the same as win version. Please keep them in same.
    env: Environment = get_env()
    path_list = env.paths
    env_vars = env.vars
    for key, val in env_vars.items():
        if key == "PATH":
            continue
        if resolve:
            val = os.path.expandvars(val)
        os.environ[key] = val
    if resolve:
        path_list = [os.path.expandvars(path) for path in path_list]
    path_list = remove_adjascent_duplicates(path_list)
    path_list = [path.strip() for path in path_list if path.strip()]
    path_list_str = os.path.pathsep.join(path_list)
    path_list_str = path_list_str.replace(os.path.sep + os.path.sep, os.path.sep)
    if path_list_str.endswith(os.path.pathsep):
        path_list_str = path_list_str[:-1]
    os.environ["PATH"] = path_list_str
    if verbose:
        print(f"Setting PATH to {path_list_str}")


def get_env() -> Environment:
    """Returns the environment."""
    out = get_all_env_vars()
    return out
