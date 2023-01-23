"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel

import os
import sys
import unittest

from setenvironment import add_env_path, remove_env_path, set_env_config_file
from setenvironment.util import read_utf8

HERE = os.path.dirname(__file__)


class SetPathTester(unittest.TestCase):
    """Tester for the main module."""

    def test_setpath(self) -> None:
        """Test setting an environment variable."""
        if sys.platform != "win32":
            bashrc = os.path.join(HERE, "unix.mybashrc")
            # write a blank file
            with open(bashrc, encoding="utf-8", mode="w") as file:
                file.write("")
            set_env_config_file(bashrc)
        mypath = os.path.join("my", "path")
        add_env_path(mypath)
        print("path is now:\n", os.environ["PATH"].split(os.pathsep))
        self.assertIn(mypath, os.environ["PATH"])
        remove_env_path(mypath)
        print(f"path after removals of {mypath} is now:\n{os.environ['PATH']}")
        self.assertNotIn(mypath, os.environ["PATH"])
        if sys.platform != "win32":
            bashrc_str = read_utf8(bashrc)
            self.assertNotIn(mypath, bashrc_str)


if __name__ == "__main__":
    unittest.main()
