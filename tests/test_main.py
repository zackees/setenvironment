"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel

import sys
import os
import unittest

from setenvironment.util import read_utf8

HERE = os.path.dirname(__file__)


class MainTester(unittest.TestCase):
    """Tester for the main module."""

    @unittest.skipIf(sys.platform == "win32", "Unix only tests")
    def test_set_env_unix_macos(self) -> None:
        """Test setting an environment variable."""
        from setenvironment import setenv_unix

        bashrc = os.path.join(HERE, "unix.mybashrc")
        # write a blank file
        with open(bashrc, encoding="utf-8", mode="w") as file:
            file.write("")

        setenv_unix.get_target = lambda: bashrc  # type: ignore
        setenv_unix.set_env_var("SETENVIRONMENT_TEST", "test")
        setenv_unix.add_env_path("/my/path")
        # generate a random value
        self.assertEqual(os.environ["SETENVIRONMENT_TEST"], "test")
        self.assertIn("/my/path", os.environ["PATH"])
        setenv_unix.unset_env_var("SETENVIRONMENT_TEST")
        setenv_unix.remove_env_path("/my/path")
        self.assertNotIn("SETENVIRONMENT_TEST", os.environ)
        self.assertNotIn("/my/path", os.environ["PATH"])
        bashrc_str = read_utf8(bashrc)
        self.assertNotIn("SETENVIRONMENT_TEST", bashrc_str)
        self.assertNotIn("/my/path", bashrc_str)

    def test_cli_bindings(self) -> None:
        """Test the help option."""
        cmds = [
            "setenviroment_set",
            "setenviroment_unset",
            "setenviroment_addpath",
            "setenviroment_removepath",
        ]
        for cmd in cmds:
            help_cmd = f"{cmd} --help"
            self.assertEqual(0, os.system(help_cmd), f"Error while executing {help_cmd}")

    @unittest.skipIf(sys.platform != "win32", "Windows only tests")
    def test_env_set_win32(self) -> None:
        """Test setting an environment variable."""
        from setenvironment import setenv_win32

        setenv_win32.set_env_var("SETENVIRONMENT_TEST", "test")
        self.assertEqual(os.environ["SETENVIRONMENT_TEST"], "test")
        setenv_win32.unset_env_var("SETENVIRONMENT_TEST")
        self.assertNotIn("SETENVIRONMENT_TEST", os.environ)


if __name__ == "__main__":
    unittest.main()
