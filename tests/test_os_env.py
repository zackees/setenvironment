"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel

import os
import unittest

from setenvironment.os_env import OsEnvironment


class OsEnvironmentTester(unittest.TestCase):
    """Tester for the main module."""

    @unittest.skip("skip")
    def test_os_make_environment(self) -> None:
        """Test setting an environment variable."""
        os_env: OsEnvironment = OsEnvironment()
        print(os_env)
        data = dict(os.environ)
        paths = data["PATH"].split(os.pathsep)
        for path in os_env.paths:
            if path not in paths:
                print("path not in paths: " + path)
        data.pop("PATH", None)
        items = sorted(data.items())
        print("VARS:")
        for key, value in items:
            print(f"  {key}={value}")
        print("PATHS:")
        for path in os_env.paths:
            print(f"  {path}")
        self.fail("Force test_os_make_environment crash to read output\n" + str(os_env))

    def test_os_env_save_works(self) -> None:
        """Test that making and saving an os environment works."""
        os_env: OsEnvironment = OsEnvironment()
        os_env.vars["FOO"] = "bar"
        os_env.paths.append("my_path")
        os_env.store()
        os_env2: OsEnvironment = OsEnvironment()
        self.assertIn("FOO", os_env2.vars)
        self.assertIn("my_path", os_env2.paths)
        self.assertEqual(os_env.vars, os_env2.vars)
        self.assertEqual(os_env.paths, os_env2.paths)
        # now remove foo and my path
        del os_env.vars["FOO"]
        os_env.paths.remove("my_path")
        os_env.store()
        # now confirm they are gone
        os_env3: OsEnvironment = OsEnvironment()
        key_diff = set(os_env3.vars.keys()).difference(os_env.vars.keys())
        self.assertEqual(set(), key_diff)
        # asser list lengths are the same
        self.assertListEqual(os_env.paths, os_env3.paths)
        # assert FOO has been removed from the system environment
        self.assertNotIn("FOO", os.environ)


if __name__ == "__main__":
    unittest.main()
