"""
Test the main module
"""

# pylint: disable=fixme,import-outside-toplevel

import os
import sys
import unittest

from setenvironment import (
    add_template_path,
    get_env_var,
    get_paths,
    reload_environment,
    remove_template_group,
)
from setenvironment.testing.basetest import BASHRC, BaseTest
from setenvironment.util import read_utf8

HERE = os.path.dirname(__file__)


class TemplateGroupRemovalTester(BaseTest):
    """Tester for the main module."""

    def test_remove_template_group(self) -> None:
        """Test setting an environment variable."""
        key = "MYPATH"
        mypath = os.path.join("my", "path")
        add_template_path(key, mypath)
        reload_environment()
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
            remove_template_group(key)
        reload_environment()
        print(f"path after removals of {mypath} is now:\n{os.environ['PATH']}")
        paths = get_paths()
        self.assertNotIn(system_key, paths)
        if sys.platform != "win32":
            bashrc_str = read_utf8(BASHRC)
            self.assertNotIn(mypath, bashrc_str)


if __name__ == "__main__":
    unittest.main()
