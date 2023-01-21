"""
CLI interface for setenvironment
"""

import argparse

from .setenv import (
    set_env_var,
    get_env_var,
    add_env_path,
    unset_env_var,
    remove_env_path,
    set_env_config_file,
)


def _init_config_file(args):
    """Initialize the path to the config file."""
    if args.config_file is not None:
        set_env_config_file(args.config_file)


def setenv() -> int:
    """Set environment variables from the command line."""
    parser = argparse.ArgumentParser(description="Set environment variables")
    parser.add_argument("var_name", help="The name of the environment variable")
    parser.add_argument("var_value", help="The value of the environment variable")
    parser.add_argument("--config-file", help="The config file to use")
    args = parser.parse_args()
    _init_config_file(args)
    set_env_var(args.var_name, args.var_value)
    return 0


def getenv() -> int:
    """Get environment variables from the command line."""
    parser = argparse.ArgumentParser(description="Get environment variables")
    parser.add_argument("var_name", help="The name of the environment variable")
    parser.add_argument("--config-file", help="The config file to use")
    args = parser.parse_args()
    _init_config_file(args)
    var = get_env_var(args.var_name)
    print(var)
    return 0


def unsetenv() -> int:
    """Unset environment variables from the command line."""
    parser = argparse.ArgumentParser(description="Unset environment variables")
    parser.add_argument("var_name", help="The name of the environment variable")
    parser.add_argument("--config-file", help="The config file to use")
    args = parser.parse_args()
    _init_config_file(args)
    unset_env_var(args.var_name)
    return 0


def addpath() -> int:
    """Add a path to the PATH environment variable."""
    parser = argparse.ArgumentParser(description="Add a path to the PATH environment variable")
    parser.add_argument("path", help="The path to add")
    parser.add_argument("--config-file", help="The config file to use")
    args = parser.parse_args()
    _init_config_file(args)
    add_env_path(args.path)
    return 0


def removepath() -> int:
    """Remove a path from the PATH environment variable."""
    parser = argparse.ArgumentParser(description="Remove a path from the PATH environment variable")
    parser.add_argument("path", help="The path to remove")
    parser.add_argument("--config-file", help="The config file to use")
    args = parser.parse_args()
    _init_config_file(args)
    remove_env_path(args.path)
    return 0
