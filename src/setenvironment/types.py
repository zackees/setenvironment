import sys
import warnings
from dataclasses import dataclass


@dataclass
class Environment:
    vars: dict[str, str]
    paths: list[str]

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
