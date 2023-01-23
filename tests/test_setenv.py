"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel,R0801

import os
import random
import sys
import unittest

from setenvironment import set_env_config_file, set_env_var, unset_env_var
from setenvironment.util import read_utf8

HERE = os.path.dirname(__file__)


class SetEnvTester(unittest.TestCase):
    """Tester for the main module."""

    def test_setenv(self) -> None:
        """Test setting an environment variable."""
        if sys.platform != "win32":
            bashrc = os.path.join(HERE, "unix.mybashrc")
            # write a blank file
            with open(bashrc, encoding="utf-8", mode="w") as file:
                file.write("")
            set_env_config_file(bashrc)
        random_int = random.randint(0, 100000)
        set_env_var("SETENVIRONMENT_TEST", random_int)
        # generate a random value
        self.assertEqual(os.environ["SETENVIRONMENT_TEST"], str(random_int))
        unset_env_var("SETENVIRONMENT_TEST")
        self.assertNotIn("SETENVIRONMENT_TEST", os.environ)
        if sys.platform != "win32":
            bashrc_str = read_utf8(bashrc)
            self.assertNotIn("SETENVIRONMENT_TEST", bashrc_str)


if __name__ == "__main__":
    unittest.main()
