"""
Utility functions for setenvironment.
"""

import os


def read_utf8(path: str) -> str:
    """Reads a file as utf-8."""
    with open(path, encoding="utf-8", mode="r") as file:
        return file.read()


def write_utf8(path: str, text: str) -> None:
    """Writes a file as utf-8."""
    with open(path, encoding="utf-8", mode="w") as file:
        file.write(text)


def parse_paths(path_str: str) -> list[str]:
    """Parses a path string into a list of paths."""
    path_str = path_str.strip()
    if not path_str:
        return []
    return path_str.split(os.path.pathsep)
