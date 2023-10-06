#! /bin/bash

set -e
cd $( dirname ${BASH_SOURCE[0]})
if [ -z "$GITHUB_ACTIONS" ]; then
    . ./activate.sh
fi
echo Running ruff src tests
ruff --fix src tests
echo Running isort
isort src tests
echo Running black.
black src tests
echo Running flake8
flake8 src tests
# echo Running pylint
# pylint src  # seperate or crash happens in git-bash
echo Running mypy
mypy src tests