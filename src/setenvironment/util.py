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
    out = path_str.split(os.path.pathsep)
    out = [path for path in out if path.strip()]
    return out


def remove_adjascent_duplicates(path_list: list[str]) -> list[str]:
    """Removes adjascent duplicates."""
    out = []
    for i, path in enumerate(path_list):
        if path == "":  # also remove empty paths
            continue
        if i < len(path_list) - 1:
            a = path_list[i + 1]
            b = path_list[i]
            if a != b:
                out.append(path)
        else:
            out.append(path)
    return out
