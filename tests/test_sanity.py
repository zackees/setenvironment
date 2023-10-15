"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel

import os
import unittest


class SanityTester(unittest.TestCase):
    """Tester for the main module."""

    def test_os_make_environment(self) -> None:
        """Test setting an environment variable."""
        data = dict(os.environ)
        self.assertTrue(data)


if __name__ == "__main__":
    unittest.main()
