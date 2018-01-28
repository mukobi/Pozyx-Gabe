@echo off

wscript "send_yes.vbs"
pyinstaller --distpath PozyxGUI/pozyxgui/scripts/win 1D_ranging.py

wscript "send_yes.vbs"
pyinstaller --distpath PozyxGUI/pozyxgui/scripts/win 3D_positioning.py

wscript "send_yes.vbs"
pyinstaller --distpath PozyxGUI/pozyxgui/scripts/win motion_data.py

pause