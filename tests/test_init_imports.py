"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel

import unittest


class InitImportsTest(unittest.TestCase):
    """Tester for the main module."""

    def test(self) -> None:
        """Test setting an environment variable."""
        # fmt: off
        # isort: off
        from setenvironment import add_env_path
        from setenvironment import get_env_var
        from setenvironment import remove_env_path
        from setenvironment import set_env_config_file
        from setenvironment import set_env_var
        from setenvironment import unset_env_var
        from setenvironment import add_template_path
        from setenvironment import remove_template_path
        add_env_path = add_env_path
        get_env_var = get_env_var
        remove_env_path = remove_env_path
        set_env_config_file = set_env_config_file
        set_env_var = set_env_var
        unset_env_var = unset_env_var
        add_template_path = add_template_path
        remove_template_path = remove_template_path
        # fmt: on
        # isort: on


if __name__ == "__main__":
    unittest.main()
