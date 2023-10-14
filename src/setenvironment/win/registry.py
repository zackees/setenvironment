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
from typing import Optional

import win32gui  # type: ignore

from setenvironment.types import Environment, RegistryEnvironment
from setenvironment.win.refresh_env import REFRESH_ENV

HERE = os.path.dirname(__file__)
WIN_BIN_DIR = os.path.join(HERE, "win")
ENABLE_BROADCAST_CHANGES = False

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


def win32_registry_set_env_var_cmd_user(
    name: str, value: str, update_curr_environment=True
) -> None:
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
        win32_registry_broadcast_changes()


def win32_registry_unset_env_var_cmd_user(name: str) -> None:
    completed_proc: subprocess.CompletedProcess = _command(
        ["reg", "delete", "HKCU\\Environment", "/v", name, "/f"]
    )
    if completed_proc.returncode != 0:
        _print(f"Error happened while unsetting {name}")
        _print(get_all_user_vars())
        if completed_proc.stdout:
            _print(_try_decode(completed_proc.stdout))


def win32_registry_broadcast_changes() -> None:
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


def win32_registry_set_env_path_user(
    new_path: str, verbose=False, broad_cast_changes=True
):
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
                win32_registry_broadcast_changes()
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Failed to add path to registry because of {exc}")
        raise


def win32_registry_get_env_path_user(verbose=False) -> str:
    env: RegistryEnvironment = win32_registry_make_environment()
    path_str = os.pathsep.join(env.user.paths)
    return path_str


def win32_registry_get_env_path_system(verbose=False) -> str:
    env: RegistryEnvironment = win32_registry_make_environment()
    path_str = os.pathsep.join(env.system.paths)
    return path_str


def win32_registry_make_environment() -> RegistryEnvironment:
    user_env = get_all_user_vars()
    system_env = get_all_system_vars()
    user_path = user_env.pop("PATH", "")
    system_path = system_env.pop("PATH", "")
    user_path_list = user_path.split(os.pathsep)
    system_path_list = system_path.split(os.pathsep)
    # clear out empty strings
    user_path_list = [path for path in user_path_list if path]
    system_path_list = [path for path in system_path_list if path]
    user: Environment = Environment(vars=user_env, paths=user_path_list)
    system: Environment = Environment(vars=system_env, paths=system_path_list)
    out = RegistryEnvironment(user=user, system=system)
    return out
