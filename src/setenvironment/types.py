import json
import os
from dataclasses import dataclass

CLEAR_ENVIRONMENT = True


@dataclass
class Environment:
    vars: dict[str, str]
    paths: list[str]

    def get_var_as_pathlist(self, key: str) -> list[str]:
        """Gets a path list from an environment variable."""
        return self.vars.get(key, "").split(os.pathsep)

    def set_var_pathlist(self, key: str, path_list: list[str]) -> None:
        """Sets a path list to an environment variable, after converting to string."""
        path_list_str = os.path.pathsep.join(path_list)
        if path_list_str.endswith(os.path.pathsep):
            path_list_str = path_list_str[:-1]
        if path_list_str.startswith(os.path.pathsep):
            path_list_str = path_list_str[1:]
        self.vars[key] = path_list_str

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
        if group_path_list:
            self.set_var_pathlist(group_name, group_path_list)
        else:
            self.remove_path_group(group_name)

    def remove_path_group(self, group_name: str) -> None:
        assert group_name != "PATH"
        group_path_list = self.get_var_as_pathlist(group_name)
        for path in group_path_list:
            while path in self.paths:
                self.paths.remove(path)
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

    def to_json(self) -> str:
        """Returns a JSON representation of the object."""
        return json.dumps({"vars": self.vars, "paths": self.paths}, indent=4)


@dataclass
class BashEnvironment(Environment):
    def save(self) -> None:
        """Saves the environment."""
        from setenvironment.bash_parser import bash_save

        bash_save(self)

    def load(self) -> None:
        """Loads the environment."""
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
        self.vars = dict(os.environ)
        self.vars.pop("PATH", None)
        self.paths = [path.strip() for path in self.paths if path.strip() != ""]

    def store(self) -> None:
        """Stores the environment obj to the OS environment."""
        path_str = os.pathsep.join(self.paths)
        payload = {}
        payload.update(self.vars)
        payload["PATH"] = path_str
        # Now write it out.
        if CLEAR_ENVIRONMENT:
            os.environ.clear()
        os.environ.update(payload)


@dataclass
class RegistryEnvironment:
    user: Environment
    system: Environment

    def save(self) -> None:
        """Saves the environment."""
        from setenvironment.setenv_win32 import win32_registry_save

        win32_registry_save(self.user)

    def __str__(self) -> str:
        msg_user = str(self.user)
        msg_system = str(self.system)
        msg_user_lines = msg_user.splitlines()
        msg_system_lines = msg_system.splitlines()
        # shift everything by 4 spaces
        msg_user_lines = ["    " + line for line in msg_user_lines]
        msg_system_lines = ["    " + line for line in msg_system_lines]
        msg_user = "\n".join(msg_user_lines)
        msg_system = "\n".join(msg_system_lines)
        msg = ""
        msg += "RegistryEnvironment:\n"
        msg += "  User:\n"
        msg += msg_user
        msg += "\n"
        msg += "  System:\n"
        msg += msg_system
        return msg

    def to_json(self) -> str:
        """Returns a JSON representation of the object."""
        return json.dumps(
            {
                "user": json.loads(self.user.to_json()),
                "system": json.loads(self.system.to_json()),
            },
            indent=4,
        )
