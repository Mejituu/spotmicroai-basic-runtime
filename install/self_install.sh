#!/bin/bash

sudo apt install git python3-venv sshpass i2c-tools python-smbus joystick xboxdrv -y

grep -qxF 'options bluetooth disable_ertm=Y' /etc/modprobe.d/bluetooth.conf || echo 'options bluetooth disable_ertm=Y' | sudo tee -a /etc/modprobe.d/bluetooth.conf
cat /etc/modprobe.d/bluetooth.conf

cd ~
git clone https://gitlab.com/custom_robots/spotmicroai/basic-runtime.git spotmicroai
cd spotmicroai

chmod +x *.sh

python3 -m venv venv --clear
source venv/bin/activate

curl https://bootstrap.pypa.io/get-pip.py | python

python3 -m pip install --upgrade pip setuptools smbus jmespath adafruit-circuitpython-motor adafruit-circuitpython-pca9685 RPi.GPIO inputs

