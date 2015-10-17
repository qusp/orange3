@echo off
echo Launching NeuroPype...
set PYTHONHOME=
set "PATH=%cd%\python;%PATH%"
cd vpe
python -m Orange.canvas --clear-widget-settings