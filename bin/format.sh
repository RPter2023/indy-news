#!/usr/bin/env sh
. .venv/bin/activate

dirs="api lib pages"

echo "Formatting all code"

echo "Running isort"
python -m isort $dirs

echo "Running black"
black $dirs
