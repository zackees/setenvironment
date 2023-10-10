"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel

import os
import unittest

from setenvironment import add_env_path, reload_environment, remove_env_path

MY_PATH = os.path.join("setenvironment", "test", "path")


class ReloadEnvironmentTest(unittest.TestCase):
    def tearDown(self) -> None:
        remove_env_path(MY_PATH, update_curr_environment=False)

    def test(self) -> None:
        """Tests that we can add an environmental variable and then reload it."""
        add_env_path(MY_PATH, update_curr_environment=False)
        self.assertNotIn(MY_PATH, os.environ["PATH"])
        reload_environment()
        self.assertIn(MY_PATH, os.environ["PATH"])


if __name__ == "__main__":
    unittest.main()
