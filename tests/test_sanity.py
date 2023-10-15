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
        self.assertTrue(data)
        # os_env = OsEnvironment()
        # print(os_env)
        self.fail("Force test_os_make_environment crash to read output\n" + str(data))

    def test_get_env(self) -> None:
        """Test setting an environment variable."""
        data = get_env()
        print(data)
        self.assertTrue(data)
        self.fail("Force test_get_env crash to read output: \n" + str(data))


if __name__ == "__main__":
    unittest.main()
