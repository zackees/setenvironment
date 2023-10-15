"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel
# flake8: noqa: E501

import sys
import unittest

from setenvironment.testing.basetest import BaseTest
from setenvironment.types import OsEnvironment


class OsEnvironmentalSanity(BaseTest):
    """Tester for the main module."""
    def test_OsEnvironSanity(self) -> None:
        env = OsEnvironment()
        print(env)
        self.assertTrue(False)



if __name__ == "__main__":
    unittest.main()
