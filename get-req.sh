#!/bin/bash

echo "this script creates virtual environment for bonzo dependencies."
echo "Press enter to continue"
read -s
echo "Processing..."

python3 -m venv env

. ./env/bin/activate

pip3 install -r requirements.txt

echo $'@\n@\n@'
echo "everything went ok by far. enjoy using bonzo :^)"