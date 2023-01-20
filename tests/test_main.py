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

    @unittest.skipIf(sys.platform != "darwin", "Not macos")
    def test_set_env_macos(self) -> None:
        """Test setting an environment variable."""
        from setenvironment import setenv_macos  # pylint: disable=import-outside-toplevel

        bashrc = os.path.join(HERE, "darwin.mybashrc")
        # write a blank file
        with open(bashrc, encoding="utf-8", mode="w") as file:
            file.write("")

        setenv_macos.get_target = lambda: bashrc  # type: ignore
        setenv_macos.set_env_var("SETENVIRONMENT_TEST", "test")
        setenv_macos.add_env_path("/my/path")
        # generate a random value

        # self.assertEqual(value, int(os.environ["SETENVIRONMENT_TEST"]))
        # TODO add tests for getting the system path


if __name__ == "__main__":
    unittest.main()
