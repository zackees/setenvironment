# flake8: noqa: E501
import os
import sys
import unittest

from setenvironment import (
    add_env_path,
    get_env,
    get_env_var,
    get_paths,
    reload_environment,
    remove_env_path,
    set_env_var,
    unset_env_var,
)
from setenvironment.testing.basetest import BaseTest
from setenvironment.types import Environment, OsEnvironment


class EnvironmentTester(BaseTest):
    def test_variable(self) -> None:
        """Tests that we can add an environmental variable and then reload it."""
        # Sanity check.
        # paths = os.environ["PATH"].split(os.pathsep)
        # self.assertNotIn(MY_PATH, paths)
        # add_env_path(MY_PATH)
        set_env_var("FOO", "BAR")
        reload_environment()
        self.assertEqual(get_env_var("FOO"), "BAR")

    def test_path(self) -> None:
        """Tests that we can add an environmental variable and then reload it."""
        # Sanity check.
        # paths = os.environ["PATH"].split(os.pathsep)
        # self.assertNotIn(MY_PATH, paths)
        # add_env_path(MY_PATH)
        add_env_path("MY_PATH")
        reload_environment()
        self.assertIn("MY_PATH", get_paths())


if __name__ == "__main__":
    unittest.main()
