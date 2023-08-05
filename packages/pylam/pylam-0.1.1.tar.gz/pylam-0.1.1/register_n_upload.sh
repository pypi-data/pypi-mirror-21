#!/usr/bin/env sh

python setup.py register
python setup.py sdist upload

python setup.py build_sphinx
python setup.py upload_sphinx