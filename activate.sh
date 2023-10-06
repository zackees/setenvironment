
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
