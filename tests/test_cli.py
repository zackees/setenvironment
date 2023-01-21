"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel

import os
import unittest
import random
import subprocess

HERE = os.path.dirname(__file__)
BASHRC = os.path.join(HERE, "unix.mybashrc")


class MainTester(unittest.TestCase):
    """Tester for the main module."""

    def test_cli_bindings(self) -> None:
        """Test the help option."""
        cmds = [
            "setenvironment_set",
            "setenvironment_get",
            "setenvironment_unset",
            "setenvironment_addpath",
            "setenvironment_removepath",
        ]
        for cmd in cmds:
            help_cmd = f"{cmd} --help"
            subprocess.check_output(help_cmd, shell=True)

    def test_cli_set(self) -> None:
        """Test the set command."""
        random_int = random.randint(0, 100000)
        set_cmd = f"setenvironment_set SETENVIRONMENT_TEST {random_int} --config-file {BASHRC}"
        self.assertEqual(0, os.system(set_cmd), f"Error while executing {set_cmd}")
        value = int(
            subprocess.check_output(
                f"setenvironment_get SETENVIRONMENT_TEST --config-file {BASHRC}",
                shell=True,
            )
        )
        self.assertEqual(value, int(random_int))
        os.system(f"setenvironment_unset SETENVIRONMENT_TEST --config-file {BASHRC}")
        rtn = os.system(
            f"setenvironment_get SETENVIRONMENT_TEST --config-file {BASHRC}"
        )
        self.assertNotEqual(0, rtn)


if __name__ == "__main__":
    unittest.main()
