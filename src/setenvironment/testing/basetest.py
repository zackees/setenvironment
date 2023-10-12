# flake8: noqa: E501

import os
import sys
import unittest

from setenvironment import set_env_config_file

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TEST_DIR = os.path.join(PROJECT_ROOT, "tests")
BASHRC = os.path.join(TEST_DIR, "unix.mybashrc")


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        assert os.path.exists(
            TEST_DIR
        ), f"TEST_DIR does not exist: {TEST_DIR}, make sure you install package with -e to enabling testing"
        if sys.platform != "win32":
            # write a blank file
            with open(BASHRC, encoding="utf-8", mode="w") as file:
                file.write("")
            set_env_config_file(BASHRC)
