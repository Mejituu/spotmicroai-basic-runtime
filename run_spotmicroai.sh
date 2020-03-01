#!/bin/bash

cd ~/spotmicroai

./update_spotmicroai.sh

export PYTHONPATH=.

venv/bin/python3 spotmicro/main.py
