#!/bin/bash

cd ~
cd spotmicroai

git reset --hard HEAD
git clean -df
git checkout master
git pull

find . -type f -iname "*.sh" -exec chmod +x {} \;

~/spotmicroai/install/activate.sh
