"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel

import unittest


class InitImportsTest(unittest.TestCase):
    """Tester for the main module."""

    def test(self) -> None:
        """Test setting an environment variable."""
        from setenvironment import add_env_path
        from setenvironment import get_env_var
        from setenvironment import remove_env_path
        from setenvironment import set_env_config_file
        from setenvironment import set_env_var
        from setenvironment import unset_env_var
        from setenvironment import add_template_path
        from setenvironment import remove_template_path


        


if __name__ == "__main__":
    unittest.main()
