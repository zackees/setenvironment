"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel,line-too-long
# flake8: noqa: E501
import os
import sys
import unittest

from setenvironment import (
    add_env_path,
    get_env,
    reload_environment,
    remove_env_path,
    set_env_var,
    unset_env_var,
)
from setenvironment.testing.basetest import BaseTest
from setenvironment.types import Environment, OsEnvironment

MY_PATH = os.path.join("setenvironment", "test", "path2")
MY_VAR = ("SET_ENVIRONMENT_TEST_ENV_VAR", "foo")

ORIG_OS_ENVIRON = os.environ.copy()
ORIG_PATHS = os.environ["PATH"].split(os.pathsep)


def win32_check_exists(self: BaseTest) -> None:
    """Check that we are on win32."""
    from setenvironment.setenv_win32 import query_registry_environment
    from setenvironment.types import RegistryEnvironment

    env: RegistryEnvironment = query_registry_environment()
    sys.stderr.flush()
    sys.stdout.flush()
    print(env)
    sys.stdout.flush()
    sys.stderr.flush()
    self.assertIn(MY_PATH, env.user.paths)
    self.assertIn(MY_VAR[0], env.user.vars.keys())
    self.assertEqual(env.user.vars[MY_VAR[0]], MY_VAR[1])


def unix_check_exists(self: BaseTest) -> None:
    """Check that we are on unix."""
    from setenvironment.bash_parser import bash_make_environment
    from setenvironment.types import BashEnvironment

    env: BashEnvironment = bash_make_environment()
    sys.stdout.flush()
    print(env)
    sys.stdout.flush()
    self.assertIn(MY_PATH, env.paths)
    self.assertIn(MY_VAR[0], env.vars.keys())
    self.assertEqual(env.vars[MY_VAR[0]], MY_VAR[1])


class EnvironmentTester(BaseTest):
    def tearDown(self) -> None:
        remove_env_path(MY_PATH)
        unset_env_var(MY_VAR[0])

    def test(self) -> None:
        """Tests that we can add an environmental variable and then reload it."""
        # Sanity check.
        paths = os.environ["PATH"].split(os.pathsep)
        self.assertNotIn(MY_PATH, paths)
        add_env_path(MY_PATH)
        set_env_var(MY_VAR[0], MY_VAR[1])
        reload_environment()
        if sys.platform == "win32":
            win32_check_exists(self)
        else:
            unix_check_exists(self)
        env = get_env()
        paths = os.environ["PATH"].split(os.pathsep)
        env = get_env()
        self.assertIn(MY_PATH, paths)
        self.assertIn(MY_VAR[0], env.vars.keys())
        self.assertEqual(env.vars[MY_VAR[0]], MY_VAR[1])

    def test_remove_group_path(self) -> None:
        env: Environment = Environment({}, [])
        env.add_to_path_group("FOO", "bar")
        self.assertIn("bar", env.paths)
        self.assertIn("bar", env.vars["FOO"])
        env.remove_from_path_group("FOO", "bar")
        self.assertNotIn("bar", env.paths)
        self.assertNotIn("FOO", env.vars)

    def test_remove_group_path_osenv(self) -> None:
        env: OsEnvironment = OsEnvironment()
        env.add_to_path_group("FOO", "bar")
        self.assertIn("bar", env.paths)
        self.assertIn("bar", env.vars["FOO"])
        env.remove_from_path_group("FOO", "bar")
        env.store()
        env2 = OsEnvironment()
        self.assertNotIn("bar", env2.paths)
        self.assertNotIn("FOO", env2.vars)
        print("done")


if __name__ == "__main__":
    unittest.main()
