#!/usr/bin/env sh

rm -Rf biblib.egg-info
rm -Rf build
rm -Rf dist
rm -Rf .tox
rm -Rf .eggs
rm -Rf .cache
find . -name "*.pyc" -o -name "*.pyo" -o -name '__pycache__' | xargs rm -Rf

