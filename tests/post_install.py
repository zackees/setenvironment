"""
Post install, can we still access git? (Windows may have truncated it from the path)
"""

import os
import sys
from shutil import which

from setenvironment import reload_environment


def print_env() -> None:
    """Prints the environment."""
    os_env = os.environ.copy()
    paths = os_env.pop("PATH", "")
    print("ENVIRONMENT:")
    for key, value in sorted(os_env.items()):
        print(f"  {key}={value}")
    print("PATH:")
    for path in paths.split(os.path.pathsep):
        print(f"  {path}")


def main():
    """Main entry point for the script."""
    print_env()
    if not which("git"):
        print("git not found before reload_environment()")
        return 1
    reload_environment()
    print_env()
    if not which("git"):
        print("git not found after reload_environment()")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
