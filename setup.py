import os
import re

import setuptools

URL = "https://github.com/zackees/setenvironment"

HERE = os.path.dirname(os.path.abspath(__file__))


def get_readme() -> str:
    """Get the contents of the README file."""
    readme = os.path.join(HERE, "README.md")
    with open(readme, encoding="utf-8", mode="r") as readme_file:
        readme_lines = readme_file.readlines()
    return "".join(readme_lines)


if __name__ == "__main__":
    setuptools.setup(
        name="setenvironment",
        long_description=get_readme(),
        long_description_content_type="text/markdown",
        url=URL,
    )
