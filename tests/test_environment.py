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
    unset_env_var,
)
from setenvironment.testing.basetest import BaseTest

HERE = os.path.dirname(__file__)

MY_PATH = os.path.join("setenvironment", "test", "path2")
MY_VAR = ("SET_ENVIRONMENT_TEST_ENV_VAR", "foo")

ORIG_OS_ENVIRON = os.environ.copy()
ORIG_PATHS = os.environ["PATH"].split(os.pathsep)


class ReloadEnvironmentTest(BaseTest):
    def tearDown(self) -> None:
        remove_env_path(MY_PATH, update_curr_environment=False)
        unset_env_var(MY_VAR[0], update_curr_environment=False)

    def test(self) -> None:
        """Tests that we can add an environmental variable and then reload it."""
        # Sanity check.
        paths = os.environ["PATH"].split(os.pathsep)
        self.assertNotIn(MY_PATH, paths)
        env: Environment = get_env()
        add_env_path(MY_PATH, update_curr_environment=False)
        set_env_var(MY_VAR[0], MY_VAR[1], update_curr_environment=False)
        env = get_env()
        paths = os.environ["PATH"].split(os.pathsep)
        self.assertNotIn(MY_PATH, paths)
        env = get_env()
        self.assertIn(MY_PATH, env.paths)
        self.assertIn(MY_VAR[0], env.vars.keys())
        self.assertEqual(env.vars[MY_VAR[0]], MY_VAR[1])


if __name__ == "__main__":
    unittest.main()
