"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel
# flake8: noqa: E501

import os
import sys
import unittest

from setenvironment import add_template_path, reload_environment, remove_template_path
from setenvironment.testing.basetest import BaseTest

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
        self.assertIn(PATH_KEY, os.environ)  # Should now be in os.environ.
        self.assertIn(MY_PATH, os.environ[PATH_KEY])
        if sys.platform == "win32":
            pass
        else:
            pass
        paths = os.environ["PATH"].split(os.pathsep)
        self.assertIn(MY_PATH, paths)

    def test_two_path(self) -> None:
        """Tests that we can add an environmental variable and then reload it."""
        remove_template_path(PATH_KEY, MY_PATH, remove_if_empty=True)
        remove_template_path(PATH_KEY, MY_PATH2, remove_if_empty=True)
        self.assertNotIn(PATH_KEY, os.environ)
        add_template_path(PATH_KEY, MY_PATH, update_curr_environment=False)
        add_template_path(PATH_KEY, MY_PATH2, update_curr_environment=False)
        self.assertNotIn(PATH_KEY, os.environ)  # Should not be in os.environ yet.
        reload_environment(verbose=True)
        self.assertIn(PATH_KEY, os.environ)  # Should now be in os.environ.
        self.assertIn(MY_PATH, os.environ[PATH_KEY])
        self.assertIn(MY_PATH2, os.environ[PATH_KEY])
        if sys.platform == "win32":
            pass
        else:
            pass
        paths = os.environ["PATH"].split(os.pathsep)
        self.assertIn(MY_PATH, paths)
        self.assertIn(MY_PATH2, paths)


if __name__ == "__main__":
    unittest.main()
