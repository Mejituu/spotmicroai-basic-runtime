#!/bin/bash

cd ~
cd spotmicroai

git reset --hard HEAD
git clean -df
git checkout development
git pull

find . -type f -iname "*.sh" -exec chmod +x {} \;

~/spotmicroai/install/activate.sh
