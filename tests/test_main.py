"""
Test the main module
"""

# pylint: disable=fixme

import sys
import os
import unittest

HERE = os.path.dirname(__file__)


class MainTester(unittest.TestCase):
    """Tester for the main module."""

    @unittest.skipIf(sys.platform == "win32", "Unix only tests")
    def test_set_env_macos(self) -> None:
        """Test setting an environment variable."""
        from setenvironment import setenv_unix  # pylint: disable=import-outside-toplevel

        bashrc = os.path.join(HERE, "unix.mybashrc")
        # write a blank file
        with open(bashrc, encoding="utf-8", mode="w") as file:
            file.write("")

        setenv_unix.get_target = lambda: bashrc  # type: ignore
        setenv_unix.set_env_var("SETENVIRONMENT_TEST", "test")
        setenv_unix.add_env_path("/my/path")
        # generate a random value
        self.assertEqual(os.environ["SETENVIRONMENT_TEST"], "test")
        self.assertIn("/my/path", os.environ["PATH"])


if __name__ == "__main__":
    unittest.main()
