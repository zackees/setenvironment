from setenvironment.types import OsEnvironment


def os_env_make_environment() -> OsEnvironment:
    """Makes an environment from the OS environment."""
    return OsEnvironment()


def os_env_store(environment: OsEnvironment) -> None:
    """Stores the environment obj to the OS environment."""
    environment.store()
