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
    def test_print_failure(self) -> None:
        """Remove the environment variable."""
        from setenvironment.setenv_win32 import (
            RegistryEnvironment,
            query_registry_environment,
        )

        env: RegistryEnvironment = query_registry_environment()
        print(env)
        self.assertGreater(len(env.user.vars), 0)
        self.assertGreater(len(env.system.paths), 5)
        self.assertGreater(len(env.system.vars), 5)

    @unittest.skipIf(sys.platform != "win32", "Windows only test")
    def test_get_env_path_system_registry(self) -> None:
        """Test setting an environment variable."""
        from setenvironment.setenv_win32 import (
            get_env_path_system,
            get_env_path_user,
            parse_paths_win32,
        )

        path_str = get_env_path_system() + ";" + get_env_path_user()
        self.assertIn("C:\\Windows", path_str)
        print("done")

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

    @unittest.skipIf(sys.platform != "win32", "Windows only test")
    def test_registry_write_then_reload(self) -> None:
        """Test setting an environment variable."""
        from setenvironment.setenv import reload_environment
        from setenvironment.setenv_win32 import (
            RegistryEnvironment,
            query_registry_environment,
            win32_registry_save,
        )
        from setenvironment.types import OsEnvironment

        env_prev: RegistryEnvironment = query_registry_environment()
        env: RegistryEnvironment = query_registry_environment()
        env.user.vars["BAR"] = "FOO"
        env.user.paths.append("C:\\foo")
        win32_registry_save(env.user)
        try:
            os_env = OsEnvironment()
            self.assertNotIn("BAR", os_env.vars)
            self.assertNotIn("C:\\foo", os_env.paths)
            reload_environment()
            os_env = OsEnvironment()
            self.assertIn("BAR", os_env.vars)
            self.assertIn("C:\\foo", os_env.paths)
        finally:
            env_prev.save()


if __name__ == "__main__":
    unittest.main()
