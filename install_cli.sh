#!/usr/bin/env bash
python3 setup.py build
python3 setup.py install --record install.log
rm -rf build dist src/*.egg-info
