@echo off
title Making EXE for export

echo starting now 
dir
pushd "%~dp0"
dir

pyinstaller --onefile Nas_scanner.py
TIMEOUT 10