"""
CLI interface for setenvironment
"""

import argparse

from .setenvironment import set_env_var, add_env_path, unset_env_var, remove_env_path


def setenv() -> int:
    """Set environment variables from the command line."""
    parser = argparse.ArgumentParser(description="Set environment variables")
    parser.add_argument("var_name", help="The name of the environment variable")
    parser.add_argument("var_value", help="The value of the environment variable")
    args = parser.parse_args()
    set_env_var(args.var_name, args.var_value)
    return 0


def unsetenv() -> int:
    """Unset environment variables from the command line."""
    parser = argparse.ArgumentParser(description="Unset environment variables")
    parser.add_argument("var_name", help="The name of the environment variable")
    args = parser.parse_args()
    unset_env_var(args.var_name)
    return 0


def addpath() -> int:
    """Add a path to the PATH environment variable."""
    parser = argparse.ArgumentParser(
        description="Add a path to the PATH environment variable"
    )
    parser.add_argument("path", help="The path to add")
    args = parser.parse_args()
    add_env_path(args.path)
    return 0


def removepath() -> int:
    """Remove a path from the PATH environment variable."""
    parser = argparse.ArgumentParser(
        description="Remove a path from the PATH environment variable"
    )
    parser.add_argument("path", help="The path to remove")
    args = parser.parse_args()
    remove_env_path(args.path)
    return 0
