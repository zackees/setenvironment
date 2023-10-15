import os
import sys
import warnings

from setenvironment.types import BashEnvironment, Environment
from setenvironment.util import read_utf8, write_utf8

START_MARKER = "# START setenvironment"
END_MARKER = "# END setenvironment"

BASH_FILE_OVERRIDE: str | None = None


def __get_system_bash_file() -> str:
    if sys.platform == "win32":
        raise NotImplementedError("Windows is not supported yet.")
    for srcs in ["~/.bashrc", "~/.profile", "~/.bash_profile"]:
        # Note on github runner ubuntu please force the bashrc file to be used.
        src = os.path.expanduser(srcs)
        if os.path.exists(src):
            break
    else:
        raise FileNotFoundError("Could not find any bash config file")
    return src


def bash_rc_file() -> str:
    """Returns the target file."""
    if BASH_FILE_OVERRIDE is not None:
        return BASH_FILE_OVERRIDE
    if os.environ.get("SETENVIRONMENT_CONFIG_FILE"):
        config_file = os.environ["SETENVIRONMENT_CONFIG_FILE"]
        return os.path.expanduser(config_file)

    return __get_system_bash_file()


def bash_rc_set_file(filepath: str | None) -> None:
    """Sets the target file."""
    global BASH_FILE_OVERRIDE
    BASH_FILE_OVERRIDE = filepath
    if filepath is None:
        del os.environ["SETENVIRONMENT_CONFIG_FILE"]
        return
    os.environ["SETENVIRONMENT_CONFIG_FILE"] = filepath


def set_bash_file_lines(input_lines: list[str], shell_file: str) -> None:
    """Adds new lines to the start of the bash file in the START_MARKER
    to END_MARKER section."""
    if os.path.exists(shell_file) is False:
        # Create the file.
        with open(shell_file, encoding="utf8", mode="w") as file:
            file.write("")
    file_read = read_utf8(shell_file)
    if START_MARKER not in file_read:
        # Append markers onto this.
        file_read += "\n" + START_MARKER + "\n" + END_MARKER + "\n"
        write_utf8(shell_file, file_read)
        file_read = read_utf8(shell_file)  # read again
    orig_lines = file_read.splitlines()
    # read all lines from START_MARKER to END_MARKER
    outlines = []
    found_start_marker = False
    found_end_marker = False
    for line in orig_lines:
        if line.startswith(START_MARKER):
            outlines.append(line)
            found_start_marker = True
            outlines.extend(input_lines)
            continue
        if line.startswith(END_MARKER):
            found_end_marker = True
            outlines.append(line)
            continue
        if not found_start_marker or found_end_marker:
            outlines.append(line)
            continue
    write_utf8(shell_file, "\n".join(outlines))


def read_bash_file_lines(filepath: str) -> list[str]:
    """Reads a bash file."""
    if os.path.exists(filepath) is False:
        return []
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


def bash_append_lines(write_lines: list[str]) -> None:
    """Adds a line to the bash file."""
    lines = bash_read_lines()
    lines.extend(write_lines)
    bash_write_lines(lines)


def bash_prepend_lines(write_lines: list[str]) -> None:
    """Adds a line to the bash file."""
    lines = bash_read_lines()
    lines = write_lines + lines
    bash_write_lines(lines)


def bash_read_lines() -> list[str]:
    """Reads lines from the bash file."""
    return read_bash_file_lines(bash_rc_file())


def bash_write_lines(lines: list[str]) -> None:
    """Writes lines to the bash file."""
    set_bash_file_lines(lines, bash_rc_file())


def bash_read_variable(name: str) -> str | None:
    """Gets an environment variable."""
    lines = bash_read_lines()
    for line in lines:
        if line.startswith("export " + name + "="):
            out = line[7:].split("=")[1].strip()
            if name != "PATH":
                return out
            out = out.replace(":$PATH", "")
            return out
    return None


def bash_make_environment() -> BashEnvironment:
    """Makes an environment from the bash file."""
    lines = bash_read_lines()
    vars: dict[str, str] = {}
    paths: list[str] = []
    for line in lines:
        if line.startswith("export "):
            line = line[7:]
            if "=" not in line:
                continue
            name, value = line.split("=", 1)
            name = name.strip()
            value = value.strip()
            if name == "PATH":
                paths = value.split(":")
                paths = [p for p in paths if p.lower() != "$path"]
            else:
                vars[name] = value
    paths = [p.strip() for p in paths if p.strip()]
    return BashEnvironment(vars, paths)


def bash_save(environment: Environment) -> None:
    """Saves the environment to the bash file."""
    lines = []
    for name, value in environment.vars.items():
        lines.append(f"export {name}={value}")
    env_paths_str = ":".join(environment.paths)
    if env_paths_str.endswith(":"):
        env_paths_str = env_paths_str[:-1]
    if env_paths_str.startswith(":"):
        env_paths_str = env_paths_str[1:]
    if env_paths_str.strip():
        lines.append(f"export PATH={env_paths_str}:$PATH")
    bash_write_lines(lines)
