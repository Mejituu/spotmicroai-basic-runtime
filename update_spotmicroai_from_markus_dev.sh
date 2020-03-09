#!/bin/bash

cd ~
cd spotmicroai

git reset --hard HEAD
git clean -df
git checkout markus_dev
git pull

find . -type f -iname "*.sh" -exec chmod +x {} \;

~/spotmicroai/install/activate.sh
