#!/usr/bin/env bash
#
# Run Python checkers and formatters.

echo "Checking types ..."
pyright || exit 1

echo "Running pylint"
pylint retain || exit 1

echo "Running pycheck"
pycheck retain/*.py || exit 1

echo "Sorting imports in $i"
isort retain/*.py

echo "Formatting $i with black"
black retain/*.py
