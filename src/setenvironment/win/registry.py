# flake8: noqa: E501
import json
import os
import re
import subprocess
import sys
import warnings
import winreg  # type: ignore
from typing import Optional

import win32gui  # type: ignore

from setenvironment.types import Environment
from setenvironment.win.refresh_env import REFRESH_ENV

HERE = os.path.dirname(__file__)
WIN_BIN_DIR = os.path.join(HERE, "win")
ENABLE_BROADCAST_CHANGES = False

_DEFAULT_PRINT = print
_REGISTERLY_VALUE_PATTERN = re.compile(r"    .+    (?P<type>.+)    (?P<value>.+)*")
_ENCODINGS = ["utf-8", "cp949", "ansi"]


def _print(message):
    _DEFAULT_PRINT(f"** {message}", flush=True)


def get_all_env_vars() -> dict[str, Optional[str]]:
    env_vars: dict[str, Optional[str]] = {}
    completed_process = _command(
        ["reg", "query", "HKCU\\Environment"], capture_output=True
    )
    assert completed_process.returncode == 0, "Failed to get all env vars"
    stdout = _try_decode(completed_process.stdout)
    for line in stdout.splitlines():
        # Assuming each line in the output is of the format 'name    REG_TYPE    value'
        parts = [part.strip() for part in line.split(None, 2)]
        if len(parts) == 3:
            name, reg_type, value = parts
            env_vars[name] = value
    return env_vars


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


def query_user_env(name: str) -> Optional[str]:
    current_path = None
    completed_process = _command(
        ["reg", "query", "HKCU\\Environment", "/v", name], capture_output=True
    )
    if completed_process.returncode == 0:
        stdout = _try_decode(completed_process.stdout)
        match = _REGISTERLY_VALUE_PATTERN.search(stdout)
        if match:
            current_path = match.group("value")
            if current_path:
                current_path = current_path.strip().replace("\r", "").replace("\n", "")

    elif completed_process.returncode == 1:
        return None
    return current_path


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


def set_env_var_cmd(name: str, value: str, update_curr_environment=True) -> None:
    completed_proc: subprocess.CompletedProcess = _command(
        [
            "reg",
            "add",
            "HKCU\\Environment",
            "/t",
            "REG_EXPAND_SZ",
            "/v",
            name,
            "/d",
            value,
            "/f",
        ]
    )
    if completed_proc.returncode != 0:
        _print(f"Error happened while setting {name}={value}")
        _print(_try_decode(completed_proc.stdout))
    if update_curr_environment:
        broadcast_changes()


def unset_env_var_cmd(name: str) -> None:
    completed_proc: subprocess.CompletedProcess = _command(
        ["reg", "delete", "HKCU\\Environment", "/v", name, "/f"]
    )
    if completed_proc.returncode != 0:
        _print(f"Error happened while unsetting {name}")
        _print(get_all_env_vars())
        if completed_proc.stdout:
            _print(_try_decode(completed_proc.stdout))


def broadcast_changes() -> None:
    if not ENABLE_BROADCAST_CHANGES:
        return
    print("Broadcasting changes")
    rtn = subprocess.call("refreshenv", cwd=WIN_BIN_DIR, shell=True)
    if rtn != 0:
        warnings.warn("Failed to invoke refreshenv")

    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x001A
    SMTO_ABORTIFHUNG = 0x0002
    sParam = "Environment"

    res1, res2 = win32gui.SendMessageTimeout(
        HWND_BROADCAST, WM_SETTINGCHANGE, 0, sParam, SMTO_ABORTIFHUNG, 10000
    )
    if not res1:
        print("result: %s, %s, from SendMessageTimeout" % (bool(res1), res2))


def set_env_path_registry(new_path: str, verbose=False, broad_cast_changes=True):
    if verbose:
        print(f"&&& Setting {new_path} to Windows PATH")
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            "Environment",
            0,
            winreg.KEY_SET_VALUE,
        ) as key:
            # Set the new value of the Path key
            winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
            winreg.CloseKey(key)
            if broad_cast_changes:
                broadcast_changes()
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Failed to add path to registry because of {exc}")
        raise


def get_env_path_registry(verbose=False) -> str:
    if verbose:
        print("&&& Getting Windows PATH")

    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        "Environment",
        0,
        winreg.KEY_READ,
    ) as key:
        # Get the value of the Path key
        path = winreg.QueryValueEx(key, "PATH")[0]
        winreg.CloseKey(key)
        return path


def get_env_path_system_registry(verbose=False) -> str:
    if verbose:
        print("&&& Getting Windows System PATH")

    with winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE,
        "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment",
        0,
        winreg.KEY_READ,
    ) as key:
        # Get the value of the Path key
        path = winreg.QueryValueEx(key, "Path")[0]
        winreg.CloseKey(key)
        return path
