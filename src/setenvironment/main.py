# flake8: noqa: E501

import argparse
import os
import subprocess
import sys

from setenvironment.bash_parser import bash_rc_file, bash_rc_set_file
from setenvironment.setenv import (
    add_env_path,
    get_env,
    get_env_var,
    reload_environment,
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


def do_del(key: str) -> None:
    """Delete an environment variable."""
    unset_env_var(key)


def do_addpath(path: str) -> None:
    """Add a path to the PATH environment variable."""
    add_env_path(path)


def do_delpath(path: str) -> None:
    """Remove a path from the PATH environment variable."""
    remove_env_path(path)


def do_has(key: str) -> bool:
    """Check if an environment variable exists."""
    return get_env_var(key) is not None


def do_show() -> None:
    """Show the contents of the bashrc file."""
    if sys.platform == "win32":
        from setenvironment.setenv_win32 import query_registry_environment

        env = query_registry_environment()
        print(env.to_json())
        return
    env = get_env()
    print(env.to_json())
    return
    bashrc_path = bash_rc_file()
    with open(bashrc_path, encoding="utf8", mode="r") as f:
        contents = f.read()
    msg = f"{os.path.abspath(bashrc_path)}:\n{contents}"
    print(msg)


def do_show_bashrc() -> None:
    """Show the path to the bashrc file."""
    bashrc_path = bash_rc_file()
    with open(bashrc_path, encoding="utf8", mode="r") as f:
        contents = f.read()
    msg = f"{os.path.abspath(bashrc_path)}:\n{contents}"
    print(msg)


def do_refresh(cmd: str) -> None:
    """Refreshes from the system environment."""
    reload_environment()
    if cmd:
        subprocess.call(cmd, shell=True, env=os.environ)
    else:
        env = get_env()
        print(env.to_json())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Set environment variables from the command line."
    )
    parser.add_argument("--config", help="Path to the config file", default=None)
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Sub-command help"
    )

    parser_set = subparsers.add_parser("set", help="Set an environment variable")
    parser_set.add_argument("key", help="Name of the environment variable")
    parser_set.add_argument("value", help="Value of the environment variable")

    parser_get = subparsers.add_parser(
        "get", help="Get the value of an environment variable"
    )
    parser_get.add_argument("key", help="Name of the environment variable")

    parser_del = subparsers.add_parser("del", help="Delete an environment variable")
    parser_del.add_argument("key", help="Name of the environment variable")

    parser_addpath = subparsers.add_parser(
        "addpath", help="Add a path to the PATH environment variable"
    )
    parser_addpath.add_argument("path", help="Path to be added")

    parser_delpath = subparsers.add_parser(
        "delpath", help="Remove a path from the PATH environment variable"
    )
    parser_delpath.add_argument("path", help="Path to be removed")

    parser_has = subparsers.add_parser(
        "has", help="Check if an environment variable exists"
    )
    parser_has.add_argument("key", help="Name of the environment variable to check")

    subparsers.add_parser("show", help="Show the contents of the bashrc file")
    subparsers.add_parser("bashrc", help="Show the path to the bashrc file")
    parser_refresh = subparsers.add_parser(
        "refresh", help="Refreshes from the system environment"
    )
    parser_refresh.add_argument("cmd", nargs="?", default="")

    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()
    if args.config is not None:
        bash_rc_set_file(args.config)

    if args.command == "set":
        do_set(args.key, args.value)
    elif args.command == "get":
        print(do_get(args.key))
    elif args.command == "del":
        do_del(args.key)
    elif args.command == "addpath":
        do_addpath(args.path)
    elif args.command == "delpath":
        do_delpath(args.path)
    elif args.command == "has":
        exists = 1 if do_has(args.key) else 0
        print(exists)
    elif args.command == "show":
        do_show()
    elif args.command == "bashrc":
        do_show_bashrc()
    elif args.command == "refresh":
        do_refresh(args.cmd)

    return 0


if __name__ == "__main__":
    main()
