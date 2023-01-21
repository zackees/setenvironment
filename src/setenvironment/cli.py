"""
CLI interface for setenvironment
"""

import argparse
import os
import sys
from .util import write_utf8

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
    config = args.config_file
    if config is not None:
        set_env_config_file(config)
        if not os.path.exists(config):
            os.makedirs(os.path.dirname(config), exist_ok=True)
            write_utf8(config, "")


def setenv() -> None:
    """Set environment variables from the command line."""
    parser = argparse.ArgumentParser(description="Set environment variables")
    parser.add_argument("var_name", help="The name of the environment variable")
    parser.add_argument("var_value", help="The value of the environment variable")
    parser.add_argument("--config-file", help="The config file to use")
    args = parser.parse_args()
    _init_config_file(args)
    set_env_var(args.var_name, args.var_value)
    sys.exit(0)


def getenv() -> None:
    """Get environment variables from the command line."""
    parser = argparse.ArgumentParser(description="Get environment variables")
    parser.add_argument("var_name", help="The name of the environment variable")
    parser.add_argument("--config-file", help="The config file to use")
    args = parser.parse_args()
    _init_config_file(args)
    var = get_env_var(args.var_name)
    if var is None:
        sys.exit(1)
    print(var)
    sys.exit(0)


def unsetenv() -> None:
    """Unset environment variables from the command line."""
    parser = argparse.ArgumentParser(description="Unset environment variables")
    parser.add_argument("var_name", help="The name of the environment variable")
    parser.add_argument("--config-file", help="The config file to use")
    args = parser.parse_args()
    _init_config_file(args)
    unset_env_var(args.var_name)
    sys.exit(0)


def addpath() -> None:
    """Add a path to the PATH environment variable."""
    parser = argparse.ArgumentParser(
        description="Add a path to the PATH environment variable"
    )
    parser.add_argument("path", help="The path to add")
    parser.add_argument("--config-file", help="The config file to use")
    args = parser.parse_args()
    _init_config_file(args)
    add_env_path(args.path)
    sys.exit(0)


def removepath() -> None:
    """Remove a path from the PATH environment variable."""
    parser = argparse.ArgumentParser(
        description="Remove a path from the PATH environment variable"
    )
    parser.add_argument("path", help="The path to remove")
    parser.add_argument("--config-file", help="The config file to use")
    args = parser.parse_args()
    _init_config_file(args)
    remove_env_path(args.path)
    sys.exit(0)
