#!/bin/bash

sudo systemctl disable spotmicroai.service;

sudo systemctl daemon-reload;

sudo systemctl stop spotmicroai.service
