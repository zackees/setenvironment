# flake8: noqa: E501

import os
import sys
import unittest

from setenvironment import set_env_config_file

HERE = os.path.abspath(os.path.dirname(__file__))
BASHRC = os.path.join(HERE, "unix.mybashrc")


class BaseTest(unittest.TestCase):
    def clear_bash_rc(self) -> None:
        """Write a new bashrc file."""
        if sys.platform != "win32":
            # write a blank file
            with open(BASHRC, encoding="utf-8", mode="w") as file:
                file.write("")
            set_env_config_file(BASHRC)

    def setUp(self) -> None:
        self.clear_bash_rc()
