"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel

import sys
import unittest

from setenvironment.testing.basetest import BaseTest


class WinPathTester(BaseTest):
    """Tester for the main module."""

    # teardown
    def tearDown(self) -> None:
        """Remove the environment variable."""
        from setenvironment.setenv_win32 import get_env_path_registry

        path = get_env_path_registry()
        self.assertNotIn("value not set", path)

    @unittest.skipIf(sys.platform != "win32", "Windows only test")
    def test_get_env_path_system_registry(self) -> None:
        """Test setting an environment variable."""
        from setenvironment.setenv_win32 import (
            get_env_path_system_registry,
            parse_paths_win32,
        )

        path_str = get_env_path_system_registry()
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


if __name__ == "__main__":
    unittest.main()
