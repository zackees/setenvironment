"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel

import os
import sys
import unittest

from setenvironment.setenv import (
    add_template_path,
    get_env_var,
    get_paths,
    remove_template_path,
    set_env_config_file
)
from setenvironment.util import read_utf8

HERE = os.path.dirname(__file__)


class TemplatePathtester(unittest.TestCase):
    """Tester for the main module."""

    def test_add_template_path(self) -> None:
        """Test setting an environment variable."""
        if sys.platform != "win32":
            bashrc = os.path.join(HERE, "unix.mybashrc")
            # write a blank file
            with open(bashrc, encoding="utf-8", mode="w") as file:
                file.write("")
            set_env_config_file(bashrc)
        key = "MYPATH"
        mypath = os.path.join("my", "path")
        add_template_path(key, mypath)
        new_paths = get_paths()
        print("path is now:\n", new_paths)
        if sys.platform != "win32":
            system_key = f"${key}"
        else:
            system_key = f"%{key}%"
        try:
            self.assertIn(system_key, new_paths)
            self.assertIn(mypath, get_env_var(key) or "")
        except Exception as exc:
            print(exc)
            raise exc
        finally:
            remove_template_path(key, mypath)
        print(f"path after removals of {mypath} is now:\n{os.environ['PATH']}")
        paths = get_paths()
        self.assertNotIn(system_key, paths)
        if sys.platform != "win32":
            bashrc_str = read_utf8(bashrc)
            self.assertNotIn(mypath, bashrc_str)


if __name__ == "__main__":
    unittest.main()
