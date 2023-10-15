"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel
# flake8: noqa: E501

import os
import unittest

from setenvironment import add_template_path, reload_environment, remove_template_path
from setenvironment.testing.basetest import BaseTest
from setenvironment.types import OsEnvironment

PATH_KEY = "TEST_RELOAD_PATH"
MY_PATH = os.path.join("setenvironment", "test", "path")
MY_PATH2 = os.path.join("setenvironment", "test", "path2")
MY_VAR = ("SET_ENVIRONMENT_TEST_ENV_VAR", "foo")


class ReloadPathTemplateTest(BaseTest):
    def tearDown(self) -> None:
        remove_template_path(PATH_KEY, MY_PATH)
        remove_template_path(PATH_KEY, MY_PATH2)
        os.environ.pop(PATH_KEY, None)

    def test_one_path(self) -> None:
        """Tests that we can add an environmental variable and then reload it."""
        remove_template_path(PATH_KEY, MY_PATH)
        add_template_path(PATH_KEY, MY_PATH)
        os_env: OsEnvironment = OsEnvironment()
        self.assertIn(PATH_KEY, os_env.vars)
        self.assertIn(MY_PATH, os_env.vars[PATH_KEY])
        self.assertIn(MY_PATH, os_env.paths)

    def test_two_path(self) -> None:
        """Tests that we can add an environmental variable and then reload it."""
        remove_template_path(PATH_KEY, MY_PATH)
        remove_template_path(PATH_KEY, MY_PATH2)
        self.assertNotIn(PATH_KEY, os.environ)
        add_template_path(PATH_KEY, MY_PATH)
        add_template_path(PATH_KEY, MY_PATH2)
        reload_environment(verbose=True)
        os_env: OsEnvironment = OsEnvironment()
        self.assertIn(PATH_KEY, os_env.vars)  # Should now be in os.environ.
        self.assertIn(MY_PATH, os_env.vars[PATH_KEY])
        self.assertIn(MY_PATH2, os_env.vars[PATH_KEY])
        self.assertIn(MY_PATH, os_env.paths)
        self.assertIn(MY_PATH2, os_env.paths)

    def test_no_empty_paths(self) -> None:
        """Tests that we can add an environmental variable and then reload it."""
        remove_template_path(PATH_KEY, MY_PATH)
        add_template_path(PATH_KEY, MY_PATH)
        reload_environment(verbose=True)
        os_env: OsEnvironment = OsEnvironment()
        for path in os_env.paths:
            self.assertNotEqual(path, "")


if __name__ == "__main__":
    unittest.main()
