#!/bin/bash
echo "this script installs all required libraries to run bonzo properly."
read -p "press return to continue."
pip3 install --user -r requirements.txt
echo "@\n@\n@"
echo "everything went ok by far. enjoy using bonzo :^)"