#!/bin/bash

# if not github runner
if [ -z "$GITHUB_WORKSPACE" ]; then
    . ./activate.sh
fi


# Navigate to the directory containing your tests
cd tests

# Use Python's unittest module to discover and run tests
python -m unittest discover