import os
import sys
import warnings
from dataclasses import dataclass


@dataclass
class Environment:
    vars: dict[str, str]
    paths: list[str]

    def get_var_as_pathlist(self, key: str) -> list[str]:
        """Gets a path list from an environment variable."""
        return self.vars.get(key, "").split(os.pathsep)

    def set_var_pathlist(self, key: str, path_list: list[str]) -> None:
        """Sets a path list to an environment variable, after converting to string."""
        self.vars[key] = os.path.pathsep.join(path_list)

    def add_to_path_group(self, group_name: str, new_path: str) -> None:
        """Adds a path using the group feature."""
        assert group_name != "PATH"
        group_path_list = self.get_var_as_pathlist(group_name)
        while new_path in group_path_list:
            group_path_list.remove(new_path)
        while new_path in self.paths:
            self.paths.remove(new_path)
        group_path_list.insert(0, new_path)
        self.paths.insert(0, new_path)
        self.set_var_pathlist(group_name, group_path_list)

    def remove_from_path_group(self, group_name: str, path_to_remove: str) -> None:
        """Removes a path from a group."""
        assert group_name != "PATH"
        group_path_list = self.get_var_as_pathlist(group_name)
        while path_to_remove in group_path_list:
            group_path_list.remove(path_to_remove)
        while path_to_remove in self.paths:
            self.paths.remove(path_to_remove)
        self.set_var_pathlist(group_name, group_path_list)

    def remove_path_group(self, group_name: str) -> None:
        assert group_name != "PATH"
        group_path_list = self.get_var_as_pathlist(group_name)
        for path in group_path_list:
            while path in self.paths:
                self.paths.remove(path)
        if group_name in self.vars:
            del self.vars[group_name]

    def add_template_path(self, group_name: str, new_path: str) -> None:
        assert "%" not in group_name, "env_var should not contain %"
        assert "%" not in new_path, "new_path should not contain %"
        assert "$" not in group_name, "env_var should not contain $"
        assert "$" not in new_path, "new_path should not contain $"
        system_key = f"%{group_name}%" if sys.platform == "win32" else f"${group_name}"
        group_path_list = self.get_var_as_pathlist(group_name)
        while new_path in group_path_list:
            group_path_list.remove(new_path)
        while system_key in self.paths:
            self.paths.remove(system_key)
        group_path_list.insert(0, new_path)
        self.paths.insert(0, system_key)
        self.set_var_pathlist(group_name, group_path_list)

    def remove_template_path(self, group_name: str, path_to_remove: str) -> None:
        assert "%" not in group_name, "env_var should not contain %"
        assert "%" not in path_to_remove, "path_to_remove should not contain %"
        assert "$" not in group_name, "env_var should not contain $"
        assert "$" not in path_to_remove, "path_to_remove should not contain $"
        system_key = f"%{group_name}%" if sys.platform == "win32" else f"${group_name}"
        group_path_list = self.get_var_as_pathlist(group_name)
        while path_to_remove in group_path_list:
            group_path_list.remove(path_to_remove)
        while system_key in self.paths:
            self.paths.remove(system_key)
        if group_path_list:  # reinsert key at front.
            self.paths.insert(0, system_key)

    def remove_template_group(self, group_name: str) -> None:
        assert "%" not in group_name, "env_var should not contain %"
        assert "$" not in group_name, "env_var should not contain $"
        system_key = f"%{group_name}%" if sys.platform == "win32" else f"${group_name}"
        while system_key in self.paths:
            self.paths.remove(system_key)
        if group_name in self.vars:
            del self.vars[group_name]

    def __getitem__(self, key: str) -> str:
        # Forbidden
        raise NotImplementedError("Don't use [] operator on this object.")

    def __str__(self) -> str:
        msg = ""
        msg += "Environment:\n"
        msg += "  Vars:\n"
        for key, value in sorted(self.vars.items()):
            msg += f"    {key} = {value}\n"
        msg += "  Paths:\n"
        for path in self.paths:
            msg += f"    {path}\n"
        return msg


@dataclass
class BashEnvironment(Environment):
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
class OsEnvironment(Environment):
    """Represents the OS environment."""

    def __init__(self):
        """Constructor that initializes from the OS environment."""
        self.paths = os.environ["PATH"].split(os.pathsep)
        self.vars = os.environ.copy()
        self.vars.pop("PATH", None)
        self.paths = [path.strip() for path in self.paths if path.strip() != ""]

    def store(self) -> None:
        """Stores the environment obj to the OS environment."""
        # os.environ = environment.vars.copy()
        # find keys that don't exist and delete them
        env_keys = self.vars.keys()
        for key in os.environ.keys():
            if "path" in key.lower():
                continue
            if key not in env_keys:
                os.environ.pop(key, None)
        # now update the rest of the keys.
        os.environ.update(self.vars)
        path_str = os.pathsep.join(self.paths)
        os.environ["PATH"] = path_str


@dataclass
class RegistryEnvironment:
    user: Environment
    system: Environment

    def save(self) -> None:
        """Saves the environment."""
        from setenvironment.setenv_win32 import win32_registry_save

        win32_registry_save(self.user)
