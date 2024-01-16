@echo off

set PYTHON=%~dp0..\venv\Scripts\python.exe
set SCRIPTS=%~dp0..\scripts
set MAIN_PY=%SCRIPTS%\fbpack\main.py

set ROWS=%1
set COLS=%2
set PATH=%3

%PYTHON% %MAIN_PY% -r %ROWS% -c %COLS% -p %PATH%

if NOT ["%errorlevel%"]==["0"] pause