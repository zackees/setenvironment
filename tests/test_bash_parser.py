"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel
# flake8: noqa: E501

import os
import unittest

from setenvironment.bash_parser import (
    Environment,
    bash_make_environment,
    bash_rc_set_file,
    bash_save,
)

HERE = os.path.dirname(__file__)
BASHRC = os.path.join(HERE, "bash_parser.mybashrc")

bash_rc_set_file(BASHRC)


class BashParserTester(unittest.TestCase):
    """Tester for the main module."""

    def test_bash_env(self) -> None:
        # Should we just interact with an Environment object?
        env: Environment = bash_make_environment()
        print(env)
        env.vars["FOO"] = "bar"
        env.paths.append("/my/path")
        bash_save(env)
        env2: Environment = bash_make_environment()
        print(env2)


if __name__ == "__main__":
    unittest.main()
