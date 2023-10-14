import os
import warnings

from setenvironment.util import read_utf8, write_utf8

START_MARKER = "# START setenvironment"
END_MARKER = "# END setenvironment"


def get_bashrc() -> str:
    """Returns the target file."""
    if os.environ.get("SETENVIRONMENT_CONFIG_FILE"):
        config_file = os.environ["SETENVIRONMENT_CONFIG_FILE"]
        return os.path.expanduser(config_file)
    # Note that non-interactive shells (like those on the github ubuntu runners)
    # do not load ~/.bashrc, but load ~/.profile instead.
    for srcs in ["~/.profile", "~/.bash_profile", "~/.bashrc"]:
        src = os.path.expanduser(srcs)
        if os.path.exists(src):
            break
    else:
        raise FileNotFoundError("Could not find any bash config file")
    return src


def set_env_config_file(filepath: str) -> None:
    """Sets the target file."""
    os.environ["SETENVIRONMENT_CONFIG_FILE"] = filepath


def set_bash_file_lines(lines: list[str], filepath: str) -> None:
    """Adds new lines to the start of the bash file in the START_MARKER
    to END_MARKER section."""
    file_read = read_utf8(filepath)
    if START_MARKER not in file_read:
        file_read += "\n" + START_MARKER + "\n" + END_MARKER + "\n"
        write_utf8(filepath, file_read)
        file_read = read_utf8(filepath)  # read again
    orig_lines = file_read.splitlines()
    # read all lines from START_MARKER to END_MARKER
    outlines = []
    found_start_marker = False
    found_end_marker = False
    for line in orig_lines:
        if line.startswith(START_MARKER):
            outlines.append(line)
            found_start_marker = True
            outlines.extend(lines)
            continue
        if line.startswith(END_MARKER):
            found_end_marker = True
            outlines.append(line)
            continue
        if not found_start_marker or found_end_marker:
            outlines.append(line)
            continue
    write_utf8(filepath, "\n".join(outlines))


def read_bash_file_lines(filepath: str) -> list[str]:
    """Reads a bash file."""
    filepath = filepath
    with open(filepath, encoding="utf8", mode="r") as file:
        lines = file.read().splitlines()
    # read all lines from START_MARKER to END_MARKER
    start_index = -1
    end_index = -1
    for i, line in enumerate(lines):
        if line.startswith(START_MARKER):
            start_index = i + 1
        if line.startswith(END_MARKER):
            end_index = i
    if start_index == -1:
        return []
    if end_index == -1:
        warnings.warn(f"Could not find {END_MARKER} in {filepath}")
        return lines[start_index:]
    return lines[start_index:end_index]
