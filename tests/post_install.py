"""
Post install, can we still access git? (Windows may have truncated it from the path)
"""

import sys
from shutil import which

from setenvironment import reload_environment


def main():
    """Main entry point for the script."""
    if not which("git"):
        print("git not found before reload_environment()")
        return 1
    reload_environment()
    if not which("git"):
        print("git not found after reload_environment()")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
