#!/bin/bash

cd ~
cd spotmicroai

git reset --hard HEAD
git clean -df
git checkout markus_dev
git pull

chmod --recursive +x *.sh

~/spotmicroai/install/activate.sh
