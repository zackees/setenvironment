"""
  Quick install
  cd <YOUR DIRECTORY>
  Download and install in one line:
    curl -X GET https://raw.githubusercontent.com/zackees/make_venv/main/install.py -o install.py && python install.py


  To enter the environment run:
    source activate.sh


  Notes:
    This script is tested to work using python2 and python3 from a fresh install. The only side effect
    of running this script is that virtualenv will be globally installed if it isn't already.
"""


import argparse
import os
import shutil
import subprocess
import sys
import warnings

# This activation script adds the ability to run it from any path and also
# aliasing pip3 and python3 to pip/python so that this works across devices.
_ACTIVATE_SH = """
#!/bin/bash

# Function that computes absolute path of a file
function abs_path {
  # Navigate to the directory of the given file (silencing output) and then print
  # the present working directory followed by the base name of the file
  (cd "$(dirname '$1')" &>/dev/null && printf "%s/%s" "$PWD" "${1##*/}")
}

# Navigate to the directory where the current script resides
cd $( dirname $(abs_path ${BASH_SOURCE[0]}))


if [[ "$IN_ACTIVATED_ENV" == "1" ]]; then
  # If it is, set the variable 'IN_ACTIVATED_ENV' to true
  IN_ACTIVATED_ENV=true
else
  # Otherwise, set 'IN_ACTIVATED_ENV' to false
  IN_ACTIVATED_ENV=false
fi

# If the 'venv' directory doesn't exist, print a message and exit.
if [[ ! -d "venv" ]]; then
  echo "The 'venv' directory does not exist, creating..."
  if [[ "$IN_ACTIVATED_ENV" == "1" ]]; then
    echo "Cannot install a new environment while in an activated environment. Please launch a new shell and try again."
    exit 1
  fi
  # Check the operating system type.
  # If it is macOS or Linux, then create an alias 'python' for 'python3'
  # and an alias 'pip' for 'pip3'. This is helpful if python2 is the default python in the system.
  echo "OSTYPE: $OSTYPE"
  if [[ "$OSTYPE" == "darwin"* || "$OSTYPE" == "linux-gnu"* ]]; then
    python3 install.py
  else
    python install.py
  fi

  . ./venv/bin/activate
  export IN_ACTIVATED_ENV=1
  export PATH=$( dirname $(abs_path ${BASH_SOURCE[0]}))/:$PATH
  echo "Environment created."
  pip install -e .
  exit 0
fi

# Activate the Python virtual environment. 
# The environment must be created beforehand and exist in a directory named 'venv' 
# in the same directory as this script.
. ./venv/bin/activate

# Add the directory where the current script resides to the PATH variable. 
# This allows executing files from that directory without specifying the full path.
export PATH=$( dirname $(abs_path ${BASH_SOURCE[0]}))/:$PATH
"""
HERE = os.path.dirname(__file__)
os.chdir(os.path.abspath(HERE))


def _exe(cmd: str, check: bool = True) -> None:
    msg = (
        "########################################\n"
        f"# Executing '{cmd}'\n"
        "########################################\n"
    )
    print(msg)
    sys.stdout.flush()
    sys.stderr.flush()
    # os.system(cmd)
    subprocess.run(cmd, shell=True, check=check)


def is_tool(name):
    """Check whether `name` is on PATH."""
    from distutils.spawn import find_executable

    return find_executable(name) is not None


def create_virtual_environment() -> None:
    if not is_tool("virtualenv"):
        _exe("pip install virtualenv")
    # Which one is better? virtualenv or venv? This may switch later.
    _exe("virtualenv -p python310 venv")
    # _exe('python3 -m venv venv')
    # Linux/MacOS uses bin and Windows uses Script, so create
    # a soft link in order to always refer to bin for all
    # platforms.
    if sys.platform == "win32":
        target = os.path.join(HERE, "venv", "Scripts")
        link = os.path.join(HERE, "venv", "bin")
        if not os.path.exists(link):
            _exe(f'mklink /J "{link}" "{target}"', check=False)
    with open("activate.sh", encoding="utf-8", mode="w") as fd:
        fd.write(_ACTIVATE_SH)
    if sys.platform != "win32":
        _exe("chmod +x activate.sh")


def main() -> int:
    IN_ACTIVATED_ENV = os.environ.get("IN_ACTIVATED_ENV", "0") == "1"
    if IN_ACTIVATED_ENV:
        print(
            "Cannot install a new environment while in an activated environment. Please launch a new shell and try again."
        )
        return 1

    parser = argparse.ArgumentParser(description="Install the project.")
    parser.add_argument(
        "--remove", action="store_true", help="Remove the virtual environment"
    )
    args = parser.parse_args()
    if args.remove:
        print("Removing virtual environment")
        shutil.rmtree("venv", ignore_errors=True)
        return 0
    if not os.path.exists("venv"):
        create_virtual_environment()
    else:
        print(f'{os.path.abspath("venv")} already exists')
    _exe(f"bash activate.sh && pip install -e .")

    print(
        'Now use ". activate.sh" (at the project root dir) to enter into the environment.'
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
