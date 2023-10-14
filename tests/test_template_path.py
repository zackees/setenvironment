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
    remove_template_group,
    remove_template_path,
)
from setenvironment.testing.basetest import BASHRC, BaseTest
from setenvironment.types import OsEnvironment
from setenvironment.util import read_utf8

HERE = os.path.dirname(__file__)

KEY = "MYPATH"
SYSTEM_KEY = f"${KEY}" if sys.platform != "win32" else f"%{KEY}%"
MYPATH = os.path.join("my", "path")


class TemplatePathtester(BaseTest):
    """Tester for the main module."""

    def test_os_add_template_path(self) -> None:
        os_env = OsEnvironment()
        os_env.add_template_path(KEY, MYPATH)
        self.assertIn(SYSTEM_KEY, os_env.paths)
        self.assertIn(KEY, os_env.vars)
        self.assertIn(MYPATH, os_env.vars[KEY])
        os_env.remove_template_path(KEY, MYPATH)

    def test_add_template_path(self) -> None:
        """Test setting an environment variable."""
        add_template_path(KEY, MYPATH)
        try:
            os_env = OsEnvironment()
            self.assertIn(SYSTEM_KEY, os_env.paths)
            self.assertIn(KEY, os_env.vars)
            self.assertIn(MYPATH, os_env.vars[KEY])
        finally:
            remove_template_path(KEY, MYPATH)
        new_paths = get_paths()
        print("path is now:\n", new_paths)
        print("done")

    def test_add_template_path_if_empty(self) -> None:
        """Test setting an environment variable."""
        KEY = "MYPATH"
        add_template_path(KEY, MYPATH)
        new_paths = get_paths()
        print("path is now:\n", new_paths)
        if sys.platform != "win32":
            SYSTEM_KEY = f"${KEY}"
        else:
            SYSTEM_KEY = f"%{KEY}%"
        try:
            self.assertIn(MYPATH, new_paths)
            self.assertIn(MYPATH, get_env_var(KEY) or "")
        except Exception as exc:
            print(exc)
            raise exc
        finally:
            remove_template_path(KEY, MYPATH)
        print(f"path after removals of {MYPATH} is now:\n{os.environ['PATH']}")
        paths = get_paths()
        # MYPATH only had one entry and should be removed.
        self.assertNotIn(SYSTEM_KEY, paths)
        if sys.platform != "win32":
            bashrc_str = read_utf8(BASHRC)
            self.assertNotIn(MYPATH, bashrc_str)

    def test_add_template_path_if_empty_add_twice(self) -> None:
        """Test setting an environment variable."""
        KEY = "MYPATH"
        mypath2 = os.path.join("my", "path2")
        add_template_path(KEY, MYPATH)
        add_template_path(KEY, mypath2)
        new_paths = get_paths()
        print("path is now:\n", new_paths)
        if sys.platform != "win32":
            SYSTEM_KEY = f"${KEY}"
        else:
            SYSTEM_KEY = f"%{KEY}%"
        try:
            self.assertIn(MYPATH, new_paths)
            self.assertIn(MYPATH, get_env_var(KEY) or "")
        except Exception as exc:
            print(exc)
            raise exc
        finally:
            remove_template_path(KEY, MYPATH)
            is_good = SYSTEM_KEY not in get_paths()
            remove_template_path(KEY, mypath2)
        self.assertTrue(is_good, f"{SYSTEM_KEY} should not still be in path.")
        print(f"path after removals of {MYPATH} is now:\n{os.environ['PATH']}")
        paths = get_paths()
        self.assertNotIn(SYSTEM_KEY, paths)
        if sys.platform != "win32":
            bashrc_str = read_utf8(BASHRC)
            self.assertNotIn(MYPATH, bashrc_str)

    def test_remove_template_group(self) -> None:
        """Test setting an environment variable."""
        KEY = "MYPATH"
        add_template_path(KEY, MYPATH)
        new_paths = get_paths()
        print("path is now:\n", new_paths)
        if sys.platform != "win32":
            SYSTEM_KEY = f"${KEY}"
        else:
            SYSTEM_KEY = f"%{KEY}%"
        try:
            self.assertIn(MYPATH, new_paths)
            self.assertIn(MYPATH, get_env_var(KEY) or "")
        except Exception as exc:
            print(exc)
            raise exc
        finally:
            remove_template_group(KEY)
        print(f"path after removals of {MYPATH} is now:\n{os.environ['PATH']}")
        paths = get_paths()
        self.assertNotIn(SYSTEM_KEY, paths)
        if sys.platform != "win32":
            bashrc_str = read_utf8(BASHRC)
            self.assertNotIn(MYPATH, bashrc_str)


if __name__ == "__main__":
    unittest.main()
