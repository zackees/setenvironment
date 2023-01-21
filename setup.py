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
    for i, line in enumerate(readme_lines):
        if "../../" in line:
            # Transform the relative links to absolute links
            output_string = re.sub(r"(\.\./\.\.)", f"{URL}/actions", line)
            output_string = re.sub(r"(\.\./\.\.)", f"{URL}", output_string)
            readme_lines[i] = output_string
    return "".join(readme_lines)


if __name__ == "__main__":
    setuptools.setup(name="setenvironment", long_description=get_readme(), url=URL)
