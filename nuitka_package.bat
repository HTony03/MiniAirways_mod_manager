@echo off
REM Activate the virtual environment
call ./venv/Scripts/activate
python -m pip install nuitka
REM Package the Python script into a single executable file using Nuitka
REM Replace ICON_PATH with the path to your .ico file
set ICON_PATH=mgr.ico
set VERSION=0.3.1.1
set SCRIPT_PATH=src\Miniairways_mod_manager_V2-UI.py
python -m nuitka --onefile --windows-uac-admin --product-name=Miniairways_mod_manager --product-version=%VERSION% --windows-icon-from-ico=%ICON_PATH% --windows-console-mode=disable --enable-plugin=pyside6 %SCRIPT_PATH%

REM Deactivate the virtual environment
deactivate
pause
@echo on