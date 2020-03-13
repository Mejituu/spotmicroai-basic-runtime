#!/bin/bash

cd ~/spotmicroai || exit

export PYTHONPATH=.

venv/bin/python3 spotmicroai/main.py
