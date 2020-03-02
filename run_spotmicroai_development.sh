#!/bin/bash

cd ~/spotmicroai

./update_spotmicroai_from_development.sh

export PYTHONPATH=.

venv/bin/python3 spotmicro/main.py
