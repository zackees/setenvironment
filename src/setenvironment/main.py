# flake8: noqa: E501

import argparse

from setenvironment.bash_parser import bash_rc_file, bash_rc_set_file
from setenvironment.setenv import (
    add_env_path,
    get_env_var,
    remove_env_path,
    set_env_var,
    unset_env_var,
)


def do_get(key: str) -> str:
    """Get the value of an environment variable."""
    return get_env_var(key) or ""


def do_set(key: str, val: str) -> None:
    """Set an environment variable."""
    set_env_var(key, val)


def do_unset(key: str) -> None:
    """Unset an environment variable."""
    unset_env_var(key)


def do_addpath(path: str) -> None:
    """Add a path to the PATH environment variable."""
    add_env_path(path)


def do_removepath(path: str) -> None:
    """Remove a path from the PATH environment variable."""
    remove_env_path(path)


def do_show() -> None:
    """Show the contents of the bashrc file."""
    bashrc_path = bash_rc_file()
    with open(bashrc_path, encoding="utf8", mode="r") as f:
        contents = f.read()
    print(contents)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Set environment variables from the command line."
    )
    parser.add_argument("--config", help="Path to the config file", default=None)
    subparsers = parser.add_subparsers(
        dest="mode", required=True, help="Sub-command help"
    )
    parser_set = subparsers.add_parser("set", help="Set an environment variable")
    parser_set.add_argument("key", help="Name of the environment variable")
    parser_set.add_argument("value", help="Value of the environment variable")

    parser_get = subparsers.add_parser(
        "get", help="Get the value of an environment variable"
    )
    parser_get.add_argument("key", help="Name of the environment variable")
    parser_unset = subparsers.add_parser("unset", help="Unset an environment variable")
    parser_unset.add_argument("key", help="Name of the environment variable")
    parser_addpath = subparsers.add_parser(
        "addpath", help="Add a path to the PATH environment variable"
    )
    parser_addpath.add_argument("path", help="Path to be added")
    parser_removepath = subparsers.add_parser(
        "removepath", help="Remove a path from the PATH environment variable"
    )
    parser_removepath.add_argument("path", help="Path to be removed")
    subparsers.add_parser("show", help="Show the contents of the bashrc file")
    args = parser.parse_args()
    return args


def main() -> int:
    """Main entry point."""
    args = parse_args()
    if args.config is not None:
        bash_rc_set_file(args.config)
    if args.mode == "set":
        do_set(args.key, args.value)
    elif args.mode == "get":
        print(do_get(args.key))
    elif args.mode == "unset":
        do_unset(args.key)
    elif args.mode == "addpath":
        do_addpath(args.path)
    elif args.mode == "removepath":
        do_removepath(args.path)
    elif args.mode == "show":
        do_show()

    return 0


if __name__ == "__main__":
    main()
