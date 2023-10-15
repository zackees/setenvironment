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
        self.assertTrue(len(env.paths) > 5)
        self.assertTrue(len(env.vars) > 5)


if __name__ == "__main__":
    unittest.main()
