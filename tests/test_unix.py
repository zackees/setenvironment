"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel

import sys
import unittest

from setenvironment.setenv_unix import (
    END_MARKER,
    START_MARKER,
    read_bash_file_lines,
    set_bash_file_lines,
)
from setenvironment.testing.basetest import BASHRC, BaseTest
from setenvironment.util import write_utf8


class SetPathTester(BaseTest):
    """Tester for the main module."""

    @unittest.skipIf(sys.platform == "win32", "Windows does not support .bashrc")
    def test_read_bash_file_lines(self) -> None:
        """Test setting an environment variable."""
        lines = read_bash_file_lines(BASHRC)
        self.assertEqual(0, len(lines))  # Should be empty at this point.

        lines = [
            "blah blah blah",
            START_MARKER,
            "foo",
            END_MARKER,
        ]
        write_utf8(BASHRC, "\n".join(lines))
        lines = read_bash_file_lines(BASHRC)
        self.assertEqual(1, len(lines))
        self.assertEqual("foo", lines[0])

    @unittest.skipIf(sys.platform == "win32", "Windows does not support .bashrc")
    def test_(self) -> None:
        """Test setting an environment variable."""
        lines = read_bash_file_lines(BASHRC)
        self.assertEqual(0, len(lines))  # Should be empty at this point.
        new_lines = ["foo", "bar"]
        set_bash_file_lines(new_lines, BASHRC)
        lines = read_bash_file_lines(BASHRC)
        self.assertEqual(2, len(lines))
        self.assertEqual("foo", lines[0])
        self.assertEqual("bar", lines[1])


if __name__ == "__main__":
    unittest.main()
