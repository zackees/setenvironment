"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel

import os
import unittest

from setenvironment.setenv import get_env


class SanityTester(unittest.TestCase):
    """Tester for the main module."""

    def test_os_print_env(self) -> None:
        """Test setting an environment variable."""
        data = dict(os.environ)
        print(data)
        self.assertTrue(len(data) > 5)
        # os_env = OsEnvironment()
        # print(os_env)

    def test_get_env(self) -> None:
        """Test setting an environment variable."""
        data = get_env()
        print(data)
        self.assertTrue(len(data.paths) > 5)
        self.assertTrue(len(data.vars) > 5)



if __name__ == "__main__":
    unittest.main()
