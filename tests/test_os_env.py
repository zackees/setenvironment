"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel

import os
import unittest

from setenvironment.os_env import OsEnvironment, os_env_make_environment


class OsEnvironmentTester(unittest.TestCase):
    """Tester for the main module."""

    def test_os_make_environment(self) -> None:
        """Test setting an environment variable."""
        os_env: OsEnvironment = os_env_make_environment()
        self.assertTrue(os_env.vars)
        self.assertTrue(os_env.paths)

    def test_os_env_save_works(self) -> None:
        """Test that making and saving an os environment works."""
        os_env: OsEnvironment = os_env_make_environment()
        os_env.vars["FOO"] = "bar"
        os_env.paths.append("my_path")
        os_env.store()
        os_env2: OsEnvironment = os_env_make_environment()
        self.assertIn("FOO", os_env2.vars)
        self.assertIn("my_path", os_env2.paths)
        self.assertEqual(os_env.vars, os_env2.vars)
        self.assertEqual(os_env.paths, os_env2.paths)
        # now remove foo and my path
        del os_env.vars["FOO"]
        os_env.paths.remove("my_path")
        os_env.store()
        # now confirm they are gone
        os_env3: OsEnvironment = os_env_make_environment()
        key_diff = set(os_env3.vars.keys()).difference(os_env.vars.keys())
        self.assertEqual(set(), key_diff)
        # asser list lengths are the same
        self.assertListEqual(os_env.paths, os_env3.paths)
        # assert FOO has been removed from the system environment
        self.assertNotIn("FOO", os.environ)


if __name__ == "__main__":
    unittest.main()
