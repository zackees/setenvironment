# pylint: disable=missing-function-docstring,import-outside-toplevel,invalid-name,unused-argument,protected-access,c-extension-no-member,consider-using-f-string,import-error,too-many-function-args,duplicate-code
# mypy: ignore-errors
# flake8: noqa: E501

# flake8: noqa: E501
import json
import os
import re
import subprocess
import sys
import warnings
import winreg  # type: ignore

import win32gui  # type: ignore

from setenvironment.types import Environment
from setenvironment.win.refresh_env import REFRESH_ENV

HERE = os.path.dirname(__file__)
WIN_BIN_DIR = os.path.join(HERE, "win")
# ENABLE_BROADCAST_CHANGES = os.environ.get("ENABLE_BROADCAST_CHANGES", "1") == "1"
# flip the default to False
DISABLE_BROADCAST_CHANGES = (
    os.environ.get("SETENVIRONMENT_DISABLE_BROADCAST_CHANGES", "0") == "1"
)

_DEFAULT_PRINT = print
_REGISTERLY_VALUE_PATTERN = re.compile(r"    .+    (?P<type>.+)    (?P<value>.+)*")
_ENCODINGS = ["utf-8", "cp949", "ansi"]


def _print(message):
    _DEFAULT_PRINT(f"** {message}", flush=True)


def _get_environment_variables_from_registry(registry_path: str) -> dict[str, str]:
    env_vars: dict[str, str] = {}
    completed_process = _command(["reg", "query", registry_path], capture_output=True)
    assert completed_process.returncode == 0, "Failed to get all env vars"
    stdout = _try_decode(completed_process.stdout)
    for line in stdout.splitlines():
        # Assuming each line in the output is of the format 'name    REG_TYPE    value'
        parts = [part.strip() for part in line.split(None, 2)]
        if len(parts) == 3:
            name, reg_type, value = parts
            if value is not None:
                env_vars[name] = value
    return env_vars


def get_all_user_vars() -> dict[str, str]:
    return _get_environment_variables_from_registry("HKCU\\Environment")


def get_all_system_vars() -> dict[str, str]:
    return _get_environment_variables_from_registry(
        "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment"
    )


def _command(*args, **kwargs):
    return subprocess.run(*args, **kwargs)  # pylint: disable=subprocess-run-check


def _try_decode(byte_string: bytes) -> str:
    assert byte_string is not None, "byte_string should not be None"
    for encoding in _ENCODINGS:
        try:
            out = byte_string.decode(encoding)
            return out
        except UnicodeDecodeError:
            continue
        except AttributeError:
            raise
    return "Error happened"


def get_env_from_shell() -> Environment:
    python_exe = sys.executable
    cmd = (
        f'cmd /c "{REFRESH_ENV}" > nul && "{python_exe}" -m setenvironment.os_env_json'
    )
    stdout = subprocess.check_output(
        cmd, cwd=WIN_BIN_DIR, shell=True, universal_newlines=True
    )
    json_data = json.loads(stdout)
    env = json_data["ENVIRONMENT"]
    path = json_data["PATH"]
    out = Environment(paths=path, vars=env)
    return out


def win32_registry_broadcast_changes() -> None:
    if DISABLE_BROADCAST_CHANGES:
        return
    print("Broadcasting changes")
    #rtn = subprocess.call("refreshenv", cwd=WIN_BIN_DIR, shell=True)
    #if rtn != 0:
    #    warnings.warn("Failed to invoke refreshenv")

    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x001A
    SMTO_ABORTIFHUNG = 0x0002
    sParam = "Environment"

    res1, res2 = win32gui.SendMessageTimeout(
        HWND_BROADCAST, WM_SETTINGCHANGE, 0, sParam, SMTO_ABORTIFHUNG, 10000
    )
    if not res1:
        print("result: %s, %s, from SendMessageTimeout" % (bool(res1), res2))


def win32_registry_set_env_path_user(
    new_path: str, verbose=False, broad_cast_changes=True
) -> None:
    win32_registry_set_all_env_vars_user(
        {"PATH": new_path}, verbose, broad_cast_changes
    )


def win32_registry_set_all_env_vars_user(
    env_vars: dict[str, str],
    remove_missing_keys: bool = False,
    verbose=False,
    broad_cast_changes=True,
) -> None:
    """Sets multiple environment variables in the Windows registry for the current user."""
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS
        ) as key:
            # If remove_missing_keys is set to True, then:
            # 1. Enumerate all environment variables in the registry
            # 2. Delete any env var that is not in the provided env_vars dictionary
            if remove_missing_keys:
                current_env_vars = {}
                index = 0
                while True:
                    try:
                        name, value, _type = winreg.EnumValue(key, index)
                        current_env_vars[name] = value
                        index += 1
                    except OSError:
                        # Reached end of registry key values
                        break

                for name in current_env_vars:
                    if name not in env_vars:
                        if verbose:
                            print(f"&&& Deleting {name}")
                        winreg.DeleteValue(key, name)

            # Set or update the values from the provided dictionary
            for name, value in env_vars.items():
                if verbose:
                    print(f"&&& Setting {name} to {value}")
                winreg.SetValueEx(key, name, 0, winreg.REG_EXPAND_SZ, value)

    except Exception as exc:  # pylint: disable=broad-except
        warnings.warn(f"An error occurred: {exc}")

    if broad_cast_changes:
        win32_registry_broadcast_changes()


def win32_registry_delete_env_vars_user(
    to_delete: set[str], verbose=False, broad_cast_changes=True
) -> None:
    """Deletes specific environment variables in the Windows registry for the current user based on provided keys."""
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS
        ) as key:
            # Delete the environment variables provided in to_delete set
            for name in to_delete:
                try:
                    if verbose:
                        print(f"&&& Deleting {name}")
                    winreg.DeleteValue(key, name)
                except FileNotFoundError:
                    # If the key doesn't exist, just skip it.
                    pass
                except Exception as exc:
                    warnings.warn(f"Failed to delete {name} because of {exc}")

    except Exception as exc:  # pylint: disable=broad-except
        warnings.warn(f"An error occurred: {exc}")

    if broad_cast_changes:
        win32_registry_broadcast_changes()
