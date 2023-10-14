import os

from setenvironment.types import OsEnvironment


def os_env_make_environment() -> OsEnvironment:
    """Makes an environment from the OS environment."""
    paths = os.environ["PATH"].split(os.pathsep)
    vars = os.environ.copy()
    vars.pop("PATH", None)
    paths = [path.strip() for path in paths if path.strip() != ""]
    return OsEnvironment(vars, paths)


def os_env_store(environment: OsEnvironment) -> None:
    """Stores the environment obj to the OS environment."""
    # os.environ = environment.vars.copy()
    # find keys that don't exist and delete them
    env_keys = environment.vars.keys()
    for key in os.environ.keys():
        if "path" in key.lower():
            continue
        if key not in env_keys:
            os.environ.pop(key, None)
    # now update the rest of the keys.
    os.environ.update(environment.vars)
    path_str = os.pathsep.join(environment.paths)
    os.environ["PATH"] = path_str


def os_update_variable(name: str, value: str) -> None:
    """Updates a variable in the OS environment."""
    os.environ[name] = value


def os_remove_variable(name: str) -> None:
    """Removes a variable from the OS environment."""
    os.environ.pop(name, None)
