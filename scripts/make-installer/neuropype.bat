@echo off
echo Launching NeuroPyPE...
call python\Scripts\activate
cd vpe
Python -m Orange.canvas --clear-widget-settings