#!/bin/bash

yes | sudo cp -rf ~/spotmicroai/systemd/spotmicroai.service /etc/systemd/system/spotmicroai.service

sudo systemctl enable spotmicroai.service;

sudo systemctl daemon-reload;

sudo systemctl restart spotmicroai.service
