@echo off

set PYTHON=%~dp0..\venv\Scripts\python.exe
set SCRIPTS=%~dp0..\scripts
set MAIN_PY=%SCRIPTS%\fbpack\main.py

set PATH=%1

%PYTHON% %MAIN_PY% -t "stagger" -p %PATH%

if NOT ["%errorlevel%"]==["0"] pause