"""
Dummy
"""

# flake8: noqa: E501

import os
from typing import Optional

from setenvironment.types import Environment
from setenvironment.util import remove_adjascent_duplicates
from setenvironment.win.registry import (
    broadcast_changes,
    get_all_user_vars,
    get_env_path_registry,
    get_env_path_system_registry,
    query_user_env,
    set_env_path_registry,
    set_env_var_cmd,
    unset_env_var_cmd,
)


def get_reg_env_path() -> str:
    path = get_env_var("PATH")
    assert path is not None, "PATH was None, which was unexpected."
    return path


def parse_paths_win32(path_str: str) -> list[str]:
    path_str = path_str.replace("/", "\\")
    paths = path_str.split(os.path.pathsep)

    def strip_trailing_slash(path: str) -> str:
        """Strips trailing slash."""
        if path.endswith("\\") or path.endswith("/"):
            return path[:-1]
        return path

    paths = [strip_trailing_slash(path) for path in paths]
    paths = [path.strip() for path in paths if path.strip()]
    return paths


def add_env_path(
    new_path: str, verbose: bool = False, update_curr_environment: bool = True
) -> None:
    new_path = str(new_path)
    new_path = new_path.replace("/", "\\")
    if verbose:
        print(f"&&& Adding {new_path} to Windows PATH:")
    current_paths = parse_paths_win32(get_env_path_registry())
    if verbose:
        print(f"Current PATH: {current_paths}")
    if verbose and new_path in current_paths:
        print(f"{new_path} already in PATH")
    else:
        current_paths.insert(0, new_path)
        current_path_str = os.path.pathsep.join(current_paths)
        set_env_path_registry(
            current_path_str, verbose=False, broad_cast_changes=update_curr_environment
        )
    os_environ_paths = parse_paths_win32(os.environ["PATH"])
    if verbose and new_path in os_environ_paths:
        print(f"{new_path} already in os.environ['PATH']")
    else:
        os_environ_paths.insert(0, new_path)
        new_env_path_str = os.path.pathsep.join(os_environ_paths)
        if update_curr_environment:
            os.environ["PATH"] = new_env_path_str


def set_env_var(
    var_name: str, var_value: str, verbose=False, update_curr_environment=True
):
    var_name = str(var_name)
    var_value = str(var_value)
    if verbose:
        print(f"$$$ Setting {var_name} to {var_value}")
    set_env_var_cmd(
        var_name, var_value, update_curr_environment=update_curr_environment
    )
    if update_curr_environment:
        os.environ[var_name] = var_value


def unset_env_var(var_name: str, verbose=False):
    var_name = str(var_name)
    if verbose:
        print(f"$$$ Unsetting {var_name}")
    if var_name == "PATH":
        raise ValueError("Cannot unset PATH")
    unset_env_var_cmd(var_name)
    try:
        os.environ.pop(var_name)
    except KeyError:
        pass


def remove_env_path(path_to_remove: str, verbose=False, update_curr_environment=True):
    # convert / to \\ for Windows
    path_to_remove = path_to_remove.replace("/", "\\")
    path_str = get_env_path_registry()
    if path_to_remove not in path_str:
        if verbose:
            print(f"{path_to_remove} not in PATH which is\n{path_str}")
        return
    paths = parse_paths_win32(path_str)
    paths = [path for path in paths if path != path_to_remove]
    sep = os.path.pathsep
    new_path_str = sep.join(paths)
    set_env_path_registry(
        new_path_str, verbose=verbose, broad_cast_changes=update_curr_environment
    )
    os_environ_paths = parse_paths_win32(os.environ["PATH"])
    os_environ_paths = [path for path in os_environ_paths if path != path_to_remove]
    new_env_path_str = sep.join(os_environ_paths)
    os.environ["PATH"] = new_env_path_str


def add_template_path(
    env_var: str, new_path: str, update_curr_environment=True
) -> None:
    assert "%" not in env_var, "env_var should not contain %"
    assert "%" not in new_path, "new_path should not contain %"
    paths = parse_paths_win32(get_env_var("PATH") or "")
    tmp_env_var = f"%{env_var}%"
    something_changed = False
    if tmp_env_var not in paths:
        paths.insert(0, tmp_env_var)
        new_path_str = os.path.pathsep.join(paths)
        set_env_path_registry(new_path_str, broad_cast_changes=False)
        something_changed = True
    var_paths = parse_paths_win32(get_env_var(env_var) or "")
    if new_path not in var_paths:
        var_paths.insert(0, new_path)
        new_var_path_str = os.path.pathsep.join(var_paths)
        set_env_var(env_var, new_var_path_str, update_curr_environment=False)
        something_changed = True
    if something_changed and update_curr_environment:
        broadcast_changes()


def remove_template_path(
    env_var: str, path_to_remove: str, remove_if_empty: bool
) -> None:
    assert "%" not in env_var, "env_var should not contain %"
    assert "%" not in path_to_remove, "path_to_remove should not contain %"
    var_paths = parse_paths_win32(get_env_var(env_var) or "")
    if path_to_remove not in var_paths:
        return
    var_paths = [path for path in var_paths if path != path_to_remove]
    new_var_path_str = os.path.pathsep.join(var_paths)
    if not new_var_path_str and remove_if_empty:
        unset_env_var(env_var)
        paths = parse_paths_win32(get_env_path_registry() or "")
        if f"%{env_var}%" in paths:
            paths = [path for path in paths if path != f"%{env_var}%"]
            new_path_str = os.path.pathsep.join(paths)
            set_env_path_registry(new_path_str)
        return
    set_env_var(env_var, new_var_path_str)
    # if the path exists in the PATH, remove it
    paths = parse_paths_win32(get_env_path_registry() or "")
    if path_to_remove in paths:
        paths = [path for path in paths if path != path_to_remove]
        new_path_str = os.path.pathsep.join(paths)
        set_env_path_registry(new_path_str)
    # now also remove it from the os.environ paths
    os_environ_paths = parse_paths_win32(os.environ["PATH"])
    if path_to_remove in os_environ_paths:
        os_environ_paths = [path for path in os_environ_paths if path != path_to_remove]
        new_env_path_str = os.path.pathsep.join(os_environ_paths)
        os.environ["PATH"] = new_env_path_str


def merge_os_paths(path_list: list[str], os_env: list[str]) -> list[str]:
    """Merges os paths."""
    out = []
    for path in path_list:
        if path not in os_env:
            out.append(path)
    out.extend(os_env)
    return out


def remove_template_group(env_var: str) -> None:
    assert "%" not in env_var, "env_var should not contain %"
    var_paths = parse_paths_win32(get_env_var(env_var) or "")
    # Now remove the env var
    unset_env_var(env_var)
    if not var_paths:
        return
    for path in var_paths:
        remove_template_path(env_var, path, remove_if_empty=True)
    # Remove from system paths
    system_var = f"%{env_var}%"
    paths = parse_paths_win32(get_env_path_registry() or "")
    if system_var in paths:
        paths = [path for path in paths if path != system_var]
        new_path_str = os.path.pathsep.join(paths)
        set_env_path_registry(new_path_str)
        os.environ["PATH"] = new_path_str


def reload_environment(verbose: bool) -> None:
    """Reloads the environment."""
    # This is nearly the same as unix version. Please keep them in same.
    env: Environment = get_env(resolve=True)
    path_list = env.paths
    env_vars = env.vars
    os.environ["PATH"] = os.path.pathsep.join(path_list)
    for key, val in env_vars.items():
        if key == "PATH":
            continue
        os.environ[key] = val
    # path_list = [os.path.expandvars(path) for path in path_list]
    # path_list = [path.strip() for path in path_list if path.strip()]
    path_list = merge_os_paths(path_list, parse_paths_win32(os.environ["PATH"]))
    path_list = [path.strip() for path in path_list if path.strip()]
    path_list = remove_adjascent_duplicates(path_list)
    path_list_str = os.path.pathsep.join(path_list)
    path_list_str = path_list_str.replace(";;", ";")
    if path_list_str.endswith(os.path.pathsep):
        path_list_str = path_list_str[:-1]
    os.environ["PATH"] = path_list_str
    if verbose:
        print(f"Setting PATH to {path_list_str}")


def resolve_path(path: str) -> str:
    """Resolves a path."""
    if "%" not in path:
        return path
    path_list = parse_paths_win32(path)
    resolve_path_list = []
    for path in path_list:
        if "%" not in path:
            resolve_path_list.append(path)
            continue
        path_parts = path.split(os.sep)
        for i, part in enumerate(path_parts):
            if "%" not in part:
                continue
            part_symbol = part.strip("%")
            resolved_part = get_env_var(part_symbol, resolve=False)
            if resolved_part is None:
                # Hack, we should expand the vars from the full state. This get's
                # us past the issue with %USERPROFILE% not being substituted.
                resolved_part = os.path.expandvars(part)
            path_parts[i] = resolved_part
        resolved_path = os.sep.join(path_parts)
        resolve_path_list.append(resolved_path)

    out = os.path.pathsep.join(resolve_path_list)
    if out.endswith(os.path.pathsep):
        out = out[:-1]
    return out


def get_env_var(name: str, resolve=True) -> Optional[str]:
    current_path = query_user_env(name)
    if current_path is None:
        return None
    if resolve and "%" in current_path:
        current_path = resolve_path(current_path)
    return current_path


def get_env(resolve=False) -> Environment:
    """Returns the environment."""
    system_paths = parse_paths_win32(get_env_path_system_registry())
    user_paths = parse_paths_win32(get_env_path_registry())
    paths = user_paths + system_paths
    vars = get_all_user_vars()
    vars.pop("PATH", None)
    if resolve:
        for key, val in vars.items():
            vars[key] = resolve_path(val)
        for i, path in enumerate(paths):
            paths[i] = resolve_path(path)
    out = Environment(paths=paths, vars=vars)
    return out
