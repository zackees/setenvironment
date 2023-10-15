"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel

import sys
import unittest

from setenvironment.bash_parser import (
    END_MARKER,
    START_MARKER,
    read_bash_file_lines,
    set_bash_file_lines,
)
from setenvironment.setenv_unix import (
    add_env_path,
    get_env_vars_from_shell,
    remove_env_path,
)
from setenvironment.testing.basetest import BASHRC, BaseTest
from setenvironment.types import Environment
from setenvironment.util import write_utf8


class UnixPathTester(BaseTest):
    """Tester for the main module."""

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

    def test_setting_env_var(self) -> None:
        """Test setting an environment variable."""
        lines = read_bash_file_lines(BASHRC)
        self.assertEqual(0, len(lines))  # Should be empty at this point.
        new_lines = ["foo", "bar"]
        set_bash_file_lines(new_lines, BASHRC)
        lines = read_bash_file_lines(BASHRC)
        self.assertEqual(2, len(lines))
        self.assertEqual("foo", lines[0])
        self.assertEqual("bar", lines[1])

    @unittest.skipIf(sys.platform == "win32", "Windows does not have a shell.")
    def test_get_env_vars_from_shell(self) -> None:
        """Test setting an env variable and then reloading it fromn the shell."""
        my_path = "/my/test/path"
        add_env_path(my_path)
        try:
            out: Environment = get_env_vars_from_shell(BASHRC)
            self.assertIn(my_path, out.paths)
            print(out)
            print("done")
        finally:
            remove_env_path(my_path)

    @unittest.skipIf(sys.platform == "win32", "Windows does not have a shell.")
    def test_registry_write_then_reload(self) -> None:
        """Test setting an environment variable."""
        from setenvironment.setenv import reload_environment
        from setenvironment.setenv_unix import BashEnvironment, bash_make_environment
        from setenvironment.types import OsEnvironment

        env_prev: BashEnvironment = bash_make_environment()
        env: BashEnvironment = bash_make_environment()
        env.vars["BAR"] = "FOO"
        env.paths.append("/foo")
        env.save()
        try:
            os_env = OsEnvironment()
            self.assertNotIn("BAR", os_env.vars)
            self.assertNotIn("/foo", os_env.paths)
            reload_environment()
            os_env = OsEnvironment()
            self.assertIn("BAR", os_env.vars)
            self.assertIn("/foo", os_env.paths)
        finally:
            env_prev.save()


if __name__ == "__main__":
    unittest.main()
