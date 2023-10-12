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
MY_VAR = ("SET_ENVIRONMENT_TEST_ENV_VAR", "foo")


class ReloadPathTemplateTest(BaseTest):
    def tearDown(self) -> None:
        remove_template_path(PATH_KEY, MY_PATH)

    def test_paths(self) -> None:
        """Tests that we can add an environmental variable and then reload it."""
        remove_template_path(PATH_KEY, MY_PATH, remove_if_empty=True)
        self.assertNotIn(PATH_KEY, os.environ)
        add_template_path(PATH_KEY, MY_PATH, update_curr_environment=False)
        self.assertNotIn(PATH_KEY, os.environ)  # Should not be in os.environ yet.
        reload_environment()
        self.assertIn(PATH_KEY, os.environ)  # Should now be in os.environ.
        if sys.platform == "win32":
            system_key = f"%{PATH_KEY}%"
        else:
            system_key = f"${PATH_KEY}"
        paths = os.environ["PATH"].split(os.pathsep)
        self.assertIn(system_key, paths)


if __name__ == "__main__":
    unittest.main()
