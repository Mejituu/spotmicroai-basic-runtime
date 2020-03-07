#!/bin/bash

cd ~
cd spotmicroai

git reset --hard HEAD
git clean -df
git checkout development
git pull

chmod +x *.sh

python3 -m venv venv --clear
source venv/bin/activate

curl https://bootstrap.pypa.io/get-pip.py | python

python3 -m pip install --upgrade pip setuptools smbus jmespath adafruit-circuitpython-motor adafruit-circuitpython-pca9685 RPi.GPIO inputs pick
