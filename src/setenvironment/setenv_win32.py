"""
Dummy
"""

# flake8: noqa: E501

import os
from typing import Optional

from setenvironment.os_env import os_env_make_environment
from setenvironment.types import Environment, OsEnvironment, RegistryEnvironment
from setenvironment.util import remove_adjascent_duplicates
from setenvironment.win.registry import (
    get_all_system_vars,
    get_all_user_vars,
    win32_registry_broadcast_changes,
    win32_registry_delete_env_vars_user,
    win32_registry_set_all_env_vars_user,
    win32_registry_set_env_path_user,
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
    new_path: str,
    verbose: bool = False,
    update_curr_environment: bool = True,
    index_to_add=0,
) -> None:
    env: RegistryEnvironment = query_registry_environment()
    user_paths = env.user.paths
    while new_path in user_paths:
        user_paths.remove(new_path)
    user_paths.insert(index_to_add, new_path)
    new_path_str = path_list_to_str(user_paths)
    win32_registry_set_env_path_user(
        new_path_str, verbose=False, broad_cast_changes=update_curr_environment
    )
    if update_curr_environment:
        os.environ["PATH"] = new_path_str


def set_env_var(
    var_name: str, var_value: str, verbose=False, update_curr_environment=True
):
    var_name = str(var_name)
    var_value = str(var_value)
    if verbose:
        print(f"$$$ Setting {var_name} to {var_value}")
    data: dict[str, str] = {}
    data[var_name] = var_value
    win32_registry_set_all_env_vars_user(
        data, broad_cast_changes=update_curr_environment
    )
    if update_curr_environment:
        os.environ[var_name] = var_value


def unset_env_var(var_name: str, verbose=False):
    var_name = str(var_name)
    if verbose:
        print(f"$$$ Unsetting {var_name}")
    if var_name == "PATH":
        raise ValueError("Cannot unset PATH")
    win32_registry_delete_env_vars_user(set({var_name}))
    try:
        os.environ.pop(var_name)
    except KeyError:
        pass


def remove_env_path(path_to_remove: str, verbose=False, update_curr_environment=True):
    # convert / to \\ for Windows
    env: RegistryEnvironment = query_registry_environment()
    os_env: OsEnvironment = os_env_make_environment()
    while path_to_remove in env.user.paths:
        env.user.paths.remove(path_to_remove)
    while path_to_remove in os_env.paths:
        os_env.paths.remove(path_to_remove)
    env.save()
    os_env.store()


def merge_os_paths(path_list: list[str], os_env: list[str]) -> list[str]:
    """Merges os paths."""
    out = []
    for path in path_list:
        if path not in os_env:
            out.append(path)
    out.extend(os_env)
    return out


def path_list_to_str(path_list: list[str]) -> str:
    """Converts path list to string."""
    path_list = [path.strip() for path in path_list if path.strip()]
    path_list = remove_adjascent_duplicates(path_list)
    path_list_str = os.path.pathsep.join(path_list)
    path_list_str = path_list_str.replace(";;", ";")
    if path_list_str.endswith(os.path.pathsep):
        path_list_str = path_list_str[:-1]
    return path_list_str


def reload_environment(verbose: bool) -> None:
    """Reloads the environment."""
    # This is nearly the same as unix version. Please keep them in same.
    env: Environment = get_env(resolve=True)
    path_list = env.paths
    env_vars = env.vars
    os.environ["PATH"] = path_list_to_str(path_list)
    for key, val in env_vars.items():
        if key == "PATH":
            continue
        os.environ[key] = val
    # path_list = [os.path.expandvars(path) for path in path_list]
    # path_list = [path.strip() for path in path_list if path.strip()]
    path_list = merge_os_paths(path_list, parse_paths_win32(os.environ["PATH"]))
    path_list_str = path_list_to_str(path_list)
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
    env: RegistryEnvironment = query_registry_environment()
    if name == "PATH":
        paths_list = env.user.paths
        path_str = os.path.pathsep.join(paths_list)
        if resolve:
            path_str = resolve_path(path_str)
        return path_str
    current_value = env.user.vars.get(name, None)
    if current_value is None:
        return None
    if resolve and "%" in current_value:
        current_value = resolve_path(current_value)
    return current_value


def get_env(resolve=False) -> Environment:
    """Returns the environment."""
    system_paths = parse_paths_win32(get_env_path_system())
    user_paths = parse_paths_win32(get_env_path_user())
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


def get_env_path_user(verbose=False) -> str:
    env: RegistryEnvironment = query_registry_environment()
    path_str = os.pathsep.join(env.user.paths)
    return path_str


def get_env_path_system(verbose=False) -> str:
    env: RegistryEnvironment = query_registry_environment()
    path_str = os.pathsep.join(env.system.paths)
    return path_str


def query_registry_environment() -> RegistryEnvironment:
    user_env = get_all_user_vars()
    system_env = get_all_system_vars()
    user_path = user_env.pop("PATH", "")
    if not user_path:
        user_path = user_env.pop("Path", "")
    system_path = system_env.pop("PATH", "")
    if not system_path:
        system_path = system_env.pop("Path", "")
    user_path_list = user_path.split(os.pathsep)
    system_path_list = system_path.split(os.pathsep)
    # clear out empty strings
    user_path_list = [path for path in user_path_list if path]
    system_path_list = [path for path in system_path_list if path]
    user: Environment = Environment(vars=user_env, paths=user_path_list)
    system: Environment = Environment(vars=system_env, paths=system_path_list)
    out = RegistryEnvironment(user=user, system=system)
    return out


def win32_registry_save(user_environment: Environment) -> None:
    """Saves the user environment. Note that system environment can't be saved."""
    user_env = user_environment.vars.copy()
    user_path = user_environment.paths
    user_path_str = os.pathsep.join(user_path)
    user_env["PATH"] = user_path_str
    win32_registry_set_all_env_vars_user(
        user_env, broad_cast_changes=False, remove_missing_keys=True
    )
    win32_registry_broadcast_changes()


def add_path_group(group_name: str, new_path: str) -> None:
    """Templates are hard and not well supported by the OS.
    Add the path and then add it to the group_name as well so
    we can remove it easily"""
    assert group_name != "PATH"
    env: RegistryEnvironment = query_registry_environment()
    os_env: OsEnvironment = os_env_make_environment()
    env.user.add_to_path_group(group_name, new_path)
    os_env.add_to_path_group(group_name, new_path)
    os_env.store()
    win32_registry_save(env.user)


def remove_from_path_group(group_name: str, path_to_remove: str) -> None:
    assert group_name != "PATH"
    env: RegistryEnvironment = query_registry_environment()
    os_env: OsEnvironment = os_env_make_environment()
    env.user.remove_from_path_group(group_name, path_to_remove)
    os_env.remove_from_path_group(group_name, path_to_remove)
    os_env.store()
    win32_registry_save(env.user)


def remove_path_group(group_name: str) -> None:
    assert group_name != "PATH"
    env: RegistryEnvironment = query_registry_environment()
    os_env: OsEnvironment = os_env_make_environment()
    env.user.remove_path_group(group_name)
    os_env.remove_path_group(group_name)
    os_env.store()
    win32_registry_save(env.user)
