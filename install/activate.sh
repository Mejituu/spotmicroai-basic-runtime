#!/bin/bash

cd ~/spotmicroai

python3 -m venv venv --clear
source venv/bin/activate

curl https://bootstrap.pypa.io/get-pip.py | python

python3 -m pip install --upgrade pip setuptools smbus jmespath adafruit-circuitpython-motor adafruit-circuitpython-pca9685 RPi.GPIO inputs pick

