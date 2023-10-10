"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel,line-too-long
# flake8: noqa: E501
import os
import unittest

from setenvironment import (
    Environment,
    add_env_path,
    get_env,
    remove_env_path,
    set_env_var,
)

MY_PATH = os.path.join("setenvironment", "test", "path")
MY_VAR = ("SET_ENVIRONMENT_TEST_ENV_VAR", "foo")


class ReloadEnvironmentTest(unittest.TestCase):
    def tearDown(self) -> None:
        remove_env_path(MY_PATH, update_curr_environment=False)

    def test(self) -> None:
        """Tests that we can add an environmental variable and then reload it."""
        add_env_path(MY_PATH, update_curr_environment=False)
        set_env_var(MY_VAR[0], MY_VAR[1])
        self.assertNotIn(MY_PATH, os.environ["PATH"])
        env: Environment = get_env()
        self.assertIn(MY_PATH, env.paths)
        self.assertIn(MY_VAR[0], env.vars.keys())


if __name__ == "__main__":
    unittest.main()
