#!/bin/bash

cd ~/spotmicroai

sshpass -p $PASSWORD rsync -avz --delete --exclude '.git' --exclude-from /home/pi/spotmicroai/.gitignore $REMOTE_FOLDER /home/pi/spotmicroai/

export PYTHONPATH=.

venv/bin/python3 spotmicro/main.py
