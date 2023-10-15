"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel


import os
import unittest

from setenvironment import get_env_var, get_paths
from setenvironment.setenv import (
    add_to_path_group,
    get_env,
    reload_environment,
    remove_from_path_group,
    remove_path_group,
)
from setenvironment.testing.basetest import BaseTest
from setenvironment.types import Environment, OsEnvironment

HERE = os.path.dirname(__file__)

KEY = "PATH_GROUP_TEST"
VAL = os.path.join("my", "path")


class PathGroupTester(BaseTest):
    """Tester for the main module."""

    def test_environment_group_path(self) -> None:
        """Tests that environment has correct behavior for group path manipulation."""
        env = Environment({}, [])  # create empty environment.
        env.add_to_path_group(KEY, VAL)
        # assert VAL was added to the path and group
        self.assertIn(VAL, env.paths)
        self.assertIn(VAL, env.vars[KEY])
        # now remove it, since it's the only one, the group path should be removed too
        env.remove_from_path_group(KEY, VAL)
        self.assertNotIn(VAL, env.paths)
        tmp: str = env.vars.get(KEY, "")
        self.assertNotIn(VAL, tmp)
        # now add it back and test the remove_group_path
        env.add_to_path_group(KEY, VAL)
        env.remove_path_group(KEY)
        self.assertNotIn(VAL, env.paths)
        self.assertNotIn(KEY, env.vars)
        print("done")

    def test_environment_add_group_path_propagates_to_osenv(self) -> None:
        add_to_path_group(KEY, VAL)
        try:
            env: OsEnvironment = OsEnvironment()
            self.assertIn(VAL, env.paths)
            self.assertIn(KEY, env.vars)
            self.assertIn(VAL, env.vars[KEY])
        except Exception as exc:
            print(exc)
            raise
        finally:
            remove_path_group(KEY)
        env = OsEnvironment()
        self.assertNotIn(VAL, env.paths)
        self.assertNotIn(KEY, env.vars)
        print("done")

    def test_add_group_path(self) -> None:
        """Test setting an environment variable."""
        remove_path_group(KEY)  # ensure it is not there
        add_to_path_group(KEY, VAL)
        new_paths = get_paths()
        print("path is now:\n", new_paths)
        try:
            self.assertEqual(VAL, new_paths[0])
            path_group = get_env_var(KEY) or ""
            path_group_list = path_group.split(os.pathsep)
            self.assertEqual(VAL, path_group_list[0])
        except Exception as exc:
            print(exc)
            raise exc
        finally:
            remove_from_path_group(KEY, VAL)
        # now test the system environment to ensure they are gone
        env: OsEnvironment = OsEnvironment()
        self.assertNotIn(VAL, env.paths)
        self.assertNotIn(KEY, env.vars)
        print("done")

    def test_group_path_reload(self) -> None:
        """Test setting an environment variable and reloading it."""
        remove_path_group(KEY)
        add_to_path_group(KEY, VAL)
        reload_environment()
        env: Environment = get_env()
        os_env: OsEnvironment = OsEnvironment()
        try:
            # assert VAl is in the path
            self.assertIn(VAL, env.paths)
            # assert VAL is in the group
            self.assertIn(VAL, env.vars[KEY])
            # same for os_env
            self.assertIn(VAL, os_env.paths)
            self.assertIn(VAL, os_env.vars[KEY])
        finally:
            remove_path_group(KEY)
        reload_environment()
        env = get_env()
        os_env = OsEnvironment()
        # assert VAL is not in the path
        self.assertNotIn(VAL, env.paths)
        # assert KEY has been removed.
        self.assertNotIn(KEY, env.vars)
        # same for os_env
        self.assertNotIn(VAL, os_env.paths)
        self.assertNotIn(KEY, os_env.vars)


if __name__ == "__main__":
    unittest.main()
