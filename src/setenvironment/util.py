"""
Utility functions for setenvironment.
"""


def read_utf8(path: str) -> str:
    """Reads a file as utf-8."""
    with open(path, encoding="utf-8", mode="r") as file:
        return file.read()


def write_utf8(path: str, text: str) -> None:
    """Writes a file as utf-8."""
    with open(path, encoding="utf-8", mode="w") as file:
        file.write(text)
