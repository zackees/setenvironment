"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel,R0801

import os
import random
import sys
import unittest

from setenvironment.setenv import set_env_var, unset_env_var
from setenvironment.testing.basetest import BASHRC, BaseTest
from setenvironment.util import read_utf8


class SetEnvTester(BaseTest):
    """Tester for the main module."""

    def test_setenv(self) -> None:
        """Test setting an environment variable."""
        random_int = random.randint(0, 100000)
        set_env_var("SETENVIRONMENT_TEST", random_int)
        # generate a random value
        self.assertEqual(os.environ["SETENVIRONMENT_TEST"], str(random_int))
        unset_env_var("SETENVIRONMENT_TEST")
        self.assertNotIn("SETENVIRONMENT_TEST", os.environ)
        if sys.platform != "win32":
            bashrc_str = read_utf8(BASHRC)
            self.assertNotIn("SETENVIRONMENT_TEST", bashrc_str)


if __name__ == "__main__":
    unittest.main()
