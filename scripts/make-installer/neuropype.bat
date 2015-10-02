@echo off
echo Launching NeuroPyPE...
set PYTHONHOME=
set "PATH=%cd%\python;%PATH%"
cd vpe
python -m Orange.canvas --clear-widget-settings