"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel
# flake8: noqa: E501

import os
import unittest

from setenvironment.bash_parser import (
    BashEnvironment,
    bash_make_environment,
    bash_rc_set_file,
    bash_read_lines,
    bash_save,
)
from setenvironment.testing.basetest import BaseTest

HERE = os.path.dirname(__file__)
BASHRC = os.path.join(HERE, "bash_parser.mybashrc")

bash_rc_set_file(BASHRC)


class BashParserTester(BaseTest):
    """Tester for the main module."""

    def test_bash_env(self) -> None:
        # Should we just interact with an Environment object?
        env: BashEnvironment = bash_make_environment()
        print(env)
        env.vars["FOO"] = "bar"
        env.paths.append("/my/path")
        bash_save(env)
        env2: BashEnvironment = bash_make_environment()
        print(env2)
        print("done")

    def test_bash_two_paths(self) -> None:
        """Tests the behavior of adding two paths and how they are parsed back."""
        env: BashEnvironment = bash_make_environment()
        env.paths.append("/my/path")
        env.paths.append("/my/path2")
        bash_save(env)
        env2: BashEnvironment = bash_make_environment()
        print(env2)
        self.assertEqual(2, len(env2.paths))
        self.assertIn("/my/path", env2.paths)
        self.assertIn("/my/path2", env2.paths)

    def test_path_is_recursive(self) -> None:
        """Path should self reference."""
        env: BashEnvironment = bash_make_environment()
        env.paths.append("/my/path")
        bash_save(env)
        try:
            lines = bash_read_lines()
            self.assertEqual(1, len(lines))
            self.assertEqual(lines[0], "export PATH=/my/path:$PATH")
        finally:
            env.paths.remove("/my/path")


if __name__ == "__main__":
    unittest.main()
