"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel
# flake8: noqa: E501

import os
import unittest

from setenvironment import add_template_path, reload_environment, remove_template_path
from setenvironment.testing.basetest import BaseTest
from setenvironment.os_env import os_env_make_environment, OsEnvironment

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
        remove_template_path(PATH_KEY, MY_PATH, remove_if_empty=True)
        self.assertNotIn(PATH_KEY, os.environ)
        add_template_path(PATH_KEY, MY_PATH, update_curr_environment=False)
        self.assertNotIn(PATH_KEY, os.environ)  # Should not be in os.environ yet.
        reload_environment(verbose=True)
        os_env: OsEnvironment = os_env_make_environment()
        # self.assertIn(PATH_KEY, os.environ)  # Should now be in os.environ.
        # self.assertIn(MY_PATH, os.environ[PATH_KEY])
        # paths = os.environ["PATH"].split(os.pathsep)
        # self.assertIn(MY_PATH, paths)
        self.assertIn(PATH_KEY, os_env.vars)
        self.assertIn(MY_PATH, os_env.vars[PATH_KEY])
        self.assertIn(MY_PATH, os_env.paths)

    def test_two_path(self) -> None:
        """Tests that we can add an environmental variable and then reload it."""
        remove_template_path(PATH_KEY, MY_PATH, remove_if_empty=True)
        remove_template_path(PATH_KEY, MY_PATH2, remove_if_empty=True)
        self.assertNotIn(PATH_KEY, os.environ)
        add_template_path(PATH_KEY, MY_PATH, update_curr_environment=False)
        add_template_path(PATH_KEY, MY_PATH2, update_curr_environment=False)
        self.assertNotIn(PATH_KEY, os.environ)  # Should not be in os.environ yet.
        reload_environment(verbose=True)
        os_env: OsEnvironment = os_env_make_environment()
        self.assertIn(PATH_KEY, os_env.vars)  # Should now be in os.environ.
        self.assertIn(MY_PATH, os_env[PATH_KEY])
        self.assertIn(MY_PATH2, os_env[PATH_KEY])
        self.assertIn(MY_PATH, os_env.paths)
        self.assertIn(MY_PATH2, os_env.paths)

    def test_no_empty_paths(self) -> None:
        """Tests that we can add an environmental variable and then reload it."""
        remove_template_path(PATH_KEY, MY_PATH, remove_if_empty=True)
        add_template_path(PATH_KEY, MY_PATH, update_curr_environment=False)
        reload_environment(verbose=True)
        os_env: OsEnvironment = os_env_make_environment()
        for path in os_env.paths:
            self.assertNotEqual(path, "")


if __name__ == "__main__":
    unittest.main()
