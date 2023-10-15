"""
Adds setenv for unix.
"""

# pylint: disable=C0116
# flake8: noqa: E501

import json
import os
import subprocess
import sys
import tempfile

from setenvironment.bash_parser import bash_make_environment, bash_rc_file, bash_save
from setenvironment.types import BashEnvironment, Environment, OsEnvironment
from setenvironment.util import remove_adjascent_duplicates


def os_update_variable(name: str, value: str) -> None:
    """Updates a variable in the OS environment."""
    os.environ[name] = value


def os_remove_variable(name: str) -> None:
    """Removes a variable from the OS environment."""
    os.environ.pop(name, None)


def set_env_var(name: str, value: str, update_curr_environment=True) -> None:
    """Sets an environment variable."""
    if update_curr_environment:
        os_update_variable(name, value)
    env: BashEnvironment = bash_make_environment()
    env.vars[name] = str(value)
    bash_save(env)


def get_env_vars_from_shell(settings_file: str | None = None) -> Environment:
    # Source the provided bashrc_file, ~/.bashrc, and ~/.profile, then execute the command.
    delim = "-------- BEGIN setenviorment.os_env_json --------"
    settings_file = settings_file or bash_rc_file()
    python_exe = sys.executable
    cmd = [
        "source ~/.profile",
        f'source "{settings_file}"',
        f'echo "{delim}"',
        f'"{python_exe}" -m setenvironment.os_env_json',
    ]
    cmd_str = "; ".join(cmd)

    # Create a temporary shell script and write the command to it
    with tempfile.NamedTemporaryFile(suffix=".sh", delete=False) as tmpfile:
        tmp_filename = tmpfile.name
        tmpfile.write(cmd_str.encode("utf-8"))

    # Make the shell script executable
    os.chmod(tmp_filename, os.stat(tmp_filename).st_mode | 0o111)
    # Execute the temporary shell script
    completed_process = subprocess.run(
        ["/bin/bash", tmp_filename],
        capture_output=True,
        universal_newlines=True,
        check=True,
        env={},  # type: ignore # do not inherit parent environment},
    )

    # Cleanup: remove the temporary file
    os.remove(tmp_filename)

    stdout = completed_process.stdout
    parts = stdout.split(delim)
    if len(parts) < 2:
        raise RuntimeError("Could not parse environment from shell.")
    json_str = parts[1].strip()
    json_data = json.loads(json_str)
    paths = json_data["PATH"]
    # remove adjascent duplicates
    paths = remove_adjascent_duplicates(paths)
    out = Environment(
        vars=json_data["ENVIRONMENT"],
        paths=paths,
    )
    return out


def unset_env_var(name: str) -> None:
    """Unsets an environment variable."""
    assert "$" not in name, "name should not contain $"
    assert name.lower() != "path", "Use remove_env_path to remove from PATH"
    env: BashEnvironment = bash_make_environment()
    os_env: OsEnvironment = OsEnvironment()
    env.vars.pop(name, None)
    os_env.vars.pop(name, None)
    os_env.store()
    env.save()


def add_env_path(path: str, verbose: bool = False) -> None:
    """Adds a path to the PATH environment variable."""
    env: BashEnvironment = bash_make_environment()
    os_env: OsEnvironment = OsEnvironment()
    env.paths.append(path)
    os_env.paths.insert(0, path)
    os_env.store()
    bash_save(env)


def remove_env_path(path: str) -> None:
    """Removes a path from the PATH environment variable."""
    # remove path from os.environ['PATH'] if it does not exist
    env: BashEnvironment = bash_make_environment()
    os_env: OsEnvironment = OsEnvironment()
    if path in os_env.paths:
        os_env.paths.remove(path)
        os_env.store()
    if path in env.paths:
        env.paths.remove(path)
        bash_save(env)


def reload_environment(verbose: bool, resolve: bool) -> None:
    """Reloads the environment."""
    env: Environment = get_env()
    path_list = env.paths
    env_vars = env.vars
    os_env: OsEnvironment = OsEnvironment()
    for key, val in env_vars.items():
        if key == "PATH":
            continue
        os_env.vars[key] = val
    if resolve:
        path_list = [os.path.expandvars(path) for path in path_list]
    path_list = remove_adjascent_duplicates(path_list)
    path_list = [path.strip() for path in path_list if path.strip()]
    os_env.paths = path_list
    os_env.store()


def combine_environments(parent: Environment, child: Environment) -> Environment:
    """Combines two environments."""
    vars = parent.vars.copy()
    vars.update(child.vars)
    paths = parent.paths.copy()
    paths.extend(child.paths)
    paths = remove_adjascent_duplicates(paths)
    out = Environment(
        vars=vars,
        paths=paths,
    )
    return out


def get_env() -> Environment:
    """Returns the environment."""
    settings_file = bash_rc_file()
    shell_env: Environment = get_env_vars_from_shell(settings_file)
    bash_env: Environment = OsEnvironment()
    return combine_environments(parent=shell_env, child=bash_env)


def remove_from_path_group(group_name: str, path_to_remove: str) -> None:
    assert group_name != "PATH"
    env: BashEnvironment = bash_make_environment()
    os_env: OsEnvironment = OsEnvironment()
    env.remove_from_path_group(group_name, path_to_remove)
    os_env.remove_from_path_group(group_name, path_to_remove)
    os_env.store()
    env.save()


def remove_path_group(group_name: str) -> None:
    assert group_name != "PATH"
    env: BashEnvironment = bash_make_environment()
    os_env: OsEnvironment = OsEnvironment()
    env.remove_path_group(group_name)
    os_env.remove_path_group(group_name)
    os_env.store()
    env.save()


def add_path_group(group_name: str, new_path: str) -> None:
    assert group_name != "PATH"
    env: BashEnvironment = bash_make_environment()
    os_env: OsEnvironment = OsEnvironment()
    env.add_to_path_group(group_name, new_path)
    os_env.add_to_path_group(group_name, new_path)
    os_env.store()
    env.save()
