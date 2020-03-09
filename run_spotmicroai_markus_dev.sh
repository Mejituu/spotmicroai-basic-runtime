#!/bin/bash

cd ~/spotmicroai

./update_spotmicroai_from_markus_dev.sh

export PYTHONPATH=.

venv/bin/python3 spotmicro/main.py
