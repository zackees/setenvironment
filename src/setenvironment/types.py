import sys
import warnings
from dataclasses import dataclass


@dataclass
class BaseEnvironment:
    vars: dict[str, str]
    paths: list[str]

    def __getitem__(self, key: str) -> str:
        assert "path" != key.lower(), "Use paths attribute instead."
        return self.vars[key]


@dataclass
class BashEnvironment(BaseEnvironment):
    def save(self) -> None:
        """Saves the environment."""
        if sys.platform == "win32":
            warnings.warn("Saving environment is not supported on Windows.")
            return
        from setenvironment.bash_parser import bash_save

        bash_save(self)

    def load(self) -> None:
        """Loads the environment."""
        if sys.platform == "win32":
            warnings.warn("Loading environment is not supported on Windows.")
            return
        from setenvironment.bash_parser import bash_make_environment

        env = bash_make_environment()
        self.vars = env.vars
        self.paths = env.paths


@dataclass
class OsEnvironment(BaseEnvironment):
    """Represents the OS environment."""

    def store(self) -> None:
        """Stores the environment to the OS environment."""
        from setenvironment.os_env import os_env_store

        os_env_store(self)
