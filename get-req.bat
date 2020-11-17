@echo off
Title bonzo ExtLib Installer
echo This Batch script will install all required libraries for running bonzo
echo /
pause
pip install --user -r requirements.txt
cls
echo Everything went ok by far. Enjoy running Bonzo!
echo /
pause
