"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel

import sys
import os
import unittest
import random

from setenvironment.util import read_utf8

HERE = os.path.dirname(__file__)


class MainTester(unittest.TestCase):
    """Tester for the main module."""

    def test_set_env_unix_macos(self) -> None:
        """Test setting an environment variable."""
        from setenvironment import (
            set_env_var,
            add_env_path,
            set_env_config_file,
            remove_env_path,
            unset_env_var,
        )

        if sys.platform != "win32":
            bashrc = os.path.join(HERE, "unix.mybashrc")
            # write a blank file
            with open(bashrc, encoding="utf-8", mode="w") as file:
                file.write("")
            set_env_config_file(bashrc)
        random_int = random.randint(0, 100000)
        set_env_var("SETENVIRONMENT_TEST", random_int)
        mypath = os.path.join("my", "path")
        add_env_path(mypath)
        # generate a random value
        self.assertEqual(os.environ["SETENVIRONMENT_TEST"], str(random_int))
        self.assertIn(mypath, os.environ["PATH"])
        unset_env_var("SETENVIRONMENT_TEST")
        remove_env_path(mypath)
        self.assertNotIn("SETENVIRONMENT_TEST", os.environ)
        self.assertNotIn(mypath, os.environ["PATH"])
        if sys.platform != "win32":
            bashrc_str = read_utf8(bashrc)
            self.assertNotIn("SETENVIRONMENT_TEST", bashrc_str)
            self.assertNotIn(mypath, bashrc_str)


if __name__ == "__main__":
    unittest.main()
