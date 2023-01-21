"""
Post install, can we still access git? (Windows may have truncated it from the path)
"""

import sys
from shutil import which


def main():
    """Main entry point for the script."""
    if not which("git"):
        print("git not found")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
