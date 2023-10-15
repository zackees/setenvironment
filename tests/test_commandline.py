"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel
# flake8: noqa: E501

import os
import subprocess
import unittest

from setenvironment.testing.basetest import BaseTest


def exe(cmd: str) -> str:
    """Returns stdout of the command."""
    print(f"executing {cmd}")

    result = subprocess.run(
        cmd, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Error while executing {cmd}. Return code is {result.returncode}. Error: {result.stderr}"
        )

    return result.stdout.strip()


class CommandLineTester(BaseTest):
    """Tester for the main module."""

    def test_command_line_interface(self) -> None:
        help_output = exe("setenvironment --help")
        self.assertIn("Set environment variables from the command line", help_output)

        # Set an environment variable and check its value
        exe("setenvironment set foo bar")
        value = exe("setenvironment get foo")
        self.assertEqual(value, "bar")

        # Delete the environment variable and check its absence
        exe("setenvironment del foo")
        value = exe("setenvironment get foo")
        self.assertEqual(value, "")

        # Add a path and verify it's added to PATH
        exe("setenvironment addpath /my/path")
        path_value = exe("setenvironment get PATH")
        self.assertIn("/my/path", path_value)

        # Remove the added path and verify it's removed from PATH
        exe("setenvironment delpath /my/path")
        path_value_after_removal = exe("setenvironment get PATH")
        self.assertNotIn("/my/path", path_value_after_removal)


if __name__ == "__main__":
    unittest.main()
