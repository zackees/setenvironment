"""
Test the main module
"""

# pylint: disable=fixme

import os
import random
import unittest

from setenvironment import set_env_var


class MainTester(unittest.TestCase):
    """Tester for the main module."""

    def test_set_env(self) -> None:
        """Test setting an environment variable."""
        # generate a random value
        value = random.randint(0, 100)
        set_env_var("SETENVIRONMENT_TEST", value)
        self.assertEqual(value, int(os.environ["SETENVIRONMENT_TEST"]))
        # TODO add tests for getting the system path


if __name__ == "__main__":
    unittest.main()
