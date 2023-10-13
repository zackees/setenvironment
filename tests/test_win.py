"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel

import sys
import unittest

from setenvironment.testing.basetest import BaseTest


class WinPathTester(BaseTest):
    """Tester for the main module."""

    @unittest.skipIf(sys.platform != "win32", "Windows only test")
    def test_get_env_path_system_registry(self) -> None:
        """Test setting an environment variable."""
        from setenvironment.setenv_win32 import (
            get_env_path_system_registry,
            parse_paths_win32,
        )

        path_str = get_env_path_system_registry()
        paths = parse_paths_win32(path_str)
        for path in paths:
            print(f"  {path}")
        print("done")
        self.assertIn("C:\\Windows", paths)


if __name__ == "__main__":
    unittest.main()
