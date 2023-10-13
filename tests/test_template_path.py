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
from setenvironment.setenv import get_env
from setenvironment.testing.basetest import BASHRC, BaseTest
from setenvironment.types import Environment
from setenvironment.util import read_utf8

HERE = os.path.dirname(__file__)


class TemplatePathtester(BaseTest):
    """Tester for the main module."""

    def test_add_template_path(self) -> None:
        """Test setting an environment variable."""
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
        self.assertEqual(system_key, paths[0])  # MYPATH should be the first entry.
        if sys.platform != "win32":
            bashrc_str = read_utf8(BASHRC)
            self.assertNotIn(mypath, bashrc_str)
        environment: Environment = get_env()
        # self.assertEqual(environment.paths[0], system_key)
        index_of_system_key = environment.paths.index(system_key)
        max_index = 0 if sys.platform == "win32" else 5
        # On unix the path inserts funning things
        self.assertLessEqual(index_of_system_key, max_index)

    def test_add_template_path_if_empty(self) -> None:
        """Test setting an environment variable."""
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
            remove_template_path(key, mypath, remove_if_empty=True)
        print(f"path after removals of {mypath} is now:\n{os.environ['PATH']}")
        paths = get_paths()
        # MYPATH only had one entry and should be removed.
        self.assertNotIn(system_key, paths)
        if sys.platform != "win32":
            bashrc_str = read_utf8(BASHRC)
            self.assertNotIn(mypath, bashrc_str)

    def test_add_template_path_if_empty_add_twice(self) -> None:
        """Test setting an environment variable."""
        key = "MYPATH"
        mypath = os.path.join("my", "path")
        mypath2 = os.path.join("my", "path2")
        add_template_path(key, mypath)
        add_template_path(key, mypath2)
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
            remove_template_path(key, mypath, remove_if_empty=True)
            is_good = system_key in get_paths()
            remove_template_path(key, mypath2, remove_if_empty=True)
        self.assertTrue(is_good, f"{system_key} should still be in path.")
        print(f"path after removals of {mypath} is now:\n{os.environ['PATH']}")
        paths = get_paths()
        self.assertNotIn(system_key, paths)
        if sys.platform != "win32":
            bashrc_str = read_utf8(BASHRC)
            self.assertNotIn(mypath, bashrc_str)

    def test_remove_template_group(self) -> None:
        """Test setting an environment variable."""
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
            remove_template_group(key)
        print(f"path after removals of {mypath} is now:\n{os.environ['PATH']}")
        paths = get_paths()
        self.assertNotIn(system_key, paths)
        if sys.platform != "win32":
            bashrc_str = read_utf8(BASHRC)
            self.assertNotIn(mypath, bashrc_str)


if __name__ == "__main__":
    unittest.main()
