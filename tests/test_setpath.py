"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel

import os
import sys
import unittest

from setenvironment.setenv import add_env_path, remove_env_path
from setenvironment.testing.basetest import BASHRC, BaseTest
from setenvironment.util import read_utf8

HERE = os.path.dirname(__file__)


class SetPathTester(BaseTest):
    """Tester for the main module."""

    def test_setpath(self) -> None:
        """Test setting an environment variable."""
        mypath = os.path.join("my", "path")
        add_env_path(mypath)
        print("path is now:\n", os.environ["PATH"].split(os.pathsep))
        self.assertIn(mypath, os.environ["PATH"])
        remove_env_path(mypath)
        print(f"path after removals of {mypath} is now:\n{os.environ['PATH']}")
        self.assertNotIn(mypath, os.environ["PATH"])
        if sys.platform != "win32":
            bashrc_str = read_utf8(BASHRC)
            self.assertNotIn(mypath, bashrc_str)


if __name__ == "__main__":
    unittest.main()
