#!/bin/bash

cd ~/spotmicroai || exit

#export PASSWORD=""
#export REMOTE_FOLDER="franferri@192.168.1.104:/Users/franferri/projects/basic-runtime/"

if [ -z ${PASSWORD+x} ]; then echo "PASSWORD is unset"; else echo "PASSWORD is set to '$PASSWORD'"; fi
if [ -z ${REMOTE_FOLDER+x} ]; then echo "REMOTE_FOLDER is unset"; exit; else echo "REMOTE_FOLDER is set to '$REMOTE_FOLDER'"; fi

sshpass -p "$PASSWORD" rsync -avz -e "ssh -o StrictHostKeyChecking=no" --delete --exclude '.git' --exclude-from ~/spotmicroai/.gitignore "$REMOTE_FOLDER" ~/spotmicroai/
