"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel
# flake8: noqa: E501

import sys
import unittest

from setenvironment.testing.basetest import BaseTest


class WinPathTester(BaseTest):
    """Tester for the main module."""

    # teardown
    def tearDown(self) -> None:
        """Remove the environment variable."""
        from setenvironment.setenv_win32 import (
            RegistryEnvironment,
            query_registry_environment,
        )

        env: RegistryEnvironment = query_registry_environment()
        self.assertNotIn("value not set", env.user.paths)

    @unittest.skipIf(sys.platform != "win32", "Windows only test")
    def test_get_env_path_system_registry(self) -> None:
        """Test setting an environment variable."""
        from setenvironment.setenv_win32 import get_env_path_system, parse_paths_win32

        path_str = get_env_path_system()
        paths = parse_paths_win32(path_str)
        print("done")
        self.assertIn("C:\\Windows", paths)

    @unittest.skipIf(sys.platform != "win32", "Windows only test")
    def test_temp_dir_is_resolved(self) -> None:
        """Test setting an environment variable."""
        from setenvironment.setenv_win32 import get_env_var

        temp_dir = get_env_var("TEMP", resolve=True)
        self.assertIsNotNone(temp_dir)
        self.assertNotIn("%", str(temp_dir))
        print("done")

    @unittest.skipIf(sys.platform != "win32", "Windows only test")
    def test_registry_environment(self) -> None:
        """Test setting an environment variable."""
        from setenvironment.setenv_win32 import (
            RegistryEnvironment,
            query_registry_environment,
        )

        env: RegistryEnvironment = query_registry_environment()
        print(env)
        print("done")

    @unittest.skipIf(sys.platform != "win32", "Windows only test")
    def test_registry_manipulation(self) -> None:
        """Test setting an environment variable."""
        from setenvironment.setenv_win32 import (
            RegistryEnvironment,
            query_registry_environment,
            win32_registry_save,
        )

        env: RegistryEnvironment = query_registry_environment()
        env.user.vars["BAR"] = "FOO"
        env.user.paths.append("C:\\foo")
        win32_registry_save(env.user)
        try:
            env2 = query_registry_environment()
            self.assertIn("BAR", env2.user.vars)
            self.assertIn("C:\\foo", env2.user.paths)
            self.assertEqual("FOO", env2.user.vars["BAR"])
        finally:
            env.user.vars.pop("BAR", None)
            if "C:\\foo" in env.user.paths:
                env.user.paths.remove("C:\\foo")
            win32_registry_save(env.user)
        env3 = query_registry_environment()
        self.assertNotIn("BAR", env3.user.vars)
        self.assertNotIn("C:\\foo", env3.user.paths)


if __name__ == "__main__":
    unittest.main()
