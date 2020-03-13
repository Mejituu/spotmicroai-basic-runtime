#!/bin/bash

cd ../..

python3 -m venv venv --clear
source venv/bin/activate

curl https://bootstrap.pypa.io/get-pip.py | python

python3 -m pip install --upgrade pip setuptools
python3 -m pip install --upgrade jmespath
python3 -m pip install --upgrade adafruit-circuitpython-motor
python3 -m pip install --upgrade adafruit-circuitpython-pca9685
python3 -m pip install --upgrade inputs
python3 -m pip install --upgrade websockets
python3 -m pip install --upgrade flask

#python3 -m pip install --upgrade smbus
#python3 -m pip install --upgrade RPi.GPIO
#python3 -m pip install --upgrade inputs
