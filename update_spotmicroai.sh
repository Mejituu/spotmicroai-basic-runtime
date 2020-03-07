#!/bin/bash

cd ~
cd spotmicroai

git reset --hard HEAD
git clean -df
git checkout master
git pull

chmod --recursive +x *.sh

~/spotmicroai/install/activate.sh
