# flake8: noqa: E501

import os
import unittest

from setenvironment.bash_parser import bash_rc_set_file

HERE = os.path.abspath(os.path.dirname(__file__))
BASHRC = os.path.join(HERE, "unix.mybashrc")
bash_rc_set_file(BASHRC)


class BaseTest(unittest.TestCase):
    def clear_bash_rc(self) -> None:
        """Write a new bashrc file."""
        # write a blank file
        with open(BASHRC, encoding="utf-8", mode="w") as file:
            file.write("")

    def setUp(self) -> None:
        bash_rc_set_file(BASHRC)
        self.clear_bash_rc()

    def tearDown(self) -> None:
        bash_rc_set_file(None)
