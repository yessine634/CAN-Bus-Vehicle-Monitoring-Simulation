@echo off
setlocal
cd /d "%~dp0"
if not exist ".runtime\tmp" mkdir ".runtime\tmp"
if not exist ".runtime\matplotlib" mkdir ".runtime\matplotlib"
set "TEMP=%CD%\.runtime\tmp"
set "TMP=%TEMP%"
set "MPLCONFIGDIR=%CD%\.runtime\matplotlib"
set "MPLBACKEND=Agg"
set "PYTHONUTF8=1"
"%CD%\.venv\Scripts\python.exe" -u src\main.py
exit /b %errorlevel%
