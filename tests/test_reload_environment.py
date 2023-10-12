"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel
# flake8: noqa: E501

import os
import unittest

from setenvironment import (
    add_env_path,
    reload_environment,
    remove_env_path,
    set_env_var,
    unset_env_var,
)
from setenvironment.testing.basetest import BaseTest
from setenvironment.util import parse_paths

MY_PATH = os.path.join("setenvironment", "test", "path")
MY_VAR = ("SET_ENVIRONMENT_TEST_ENV_VAR", "foo")


class ReloadEnvironmentTest(BaseTest):
    def tearDown(self) -> None:
        remove_env_path(MY_PATH, update_curr_environment=False)
        unset_env_var(MY_VAR[0], update_curr_environment=False)

    def test_paths(self) -> None:
        """Tests that we can add an environmental variable and then reload it."""
        add_env_path(MY_PATH, update_curr_environment=False)
        self.assertNotIn(MY_PATH, os.environ["PATH"])
        reload_environment()
        self.assertIn(MY_PATH, os.environ["PATH"])

    def test_env_vars(self) -> None:
        """Tests that we can add an environmental variable and then reload it."""
        set_env_var(MY_VAR[0], MY_VAR[1], update_curr_environment=False)
        reload_environment()
        val = os.environ.get(MY_VAR[0])
        self.assertIsNotNone(val)
        self.assertIn(MY_VAR[1], str(val))

    def test_env_vars_preserved(self) -> None:
        """Tests that we can add an environmental variable and then reload it."""
        original_os_paths = parse_paths(os.environ.get("PATH", ""))
        set_env_var(MY_VAR[0], MY_VAR[1], update_curr_environment=False)
        reload_environment()
        new_os_paths = parse_paths(os.environ.get("PATH", ""))
        for path in original_os_paths:
            self.assertIn(path, new_os_paths)

    def test_adjascent_duplicates(self) -> None:
        """Tests that we can add an environmental variable and then reload it."""
        add_env_path(MY_PATH, update_curr_environment=False)
        add_env_path(MY_PATH, update_curr_environment=False)
        self.assertNotIn(MY_PATH, os.environ["PATH"])
        reload_environment()
        items = os.environ["PATH"].split(os.path.pathsep)
        for i, item in enumerate(items):
            if item == MY_PATH and i < len(items) - 1:
                a = items[i + 1]
                b = items[i]
                self.assertNotEqual(a, b)


if __name__ == "__main__":
    unittest.main()
