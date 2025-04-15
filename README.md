# marauder-uart-gui
This is a tkinter front end for sending serial commands for esp32 marauder made primarily for touchscreens.
It is a part of author's rookBox, which includes:
RPi4, caribouLite, 7inch display, huzzah32 for now.

Go give justcallmekoko a star for his work, he deserves it.


Guide to running:  
```
sudo apt install python3-full onboard
git clone https://github.com/4motionEnjoyer/marauder-uart-gui.git 
cd marauder-uart-gui/ 
./install.sh 
./run.sh 
```
To do:
- Uninstall script
- More wifi commands
- Bluetooth commands
- GUI user manual
- Remove hardcoded /dev/ttyUSB0 for ESP32 

Done:
- Dark theme 
- Along dark theme, a /reporoot/config.txt mechanism

Ideas:
- GPS integration to sw from rpi side. 
- Manual command input tab
- Improved input

------------------------------------------------------------------------
Screenshots of the UI

![alt text](https://github.com/4motionEnjoyer/marauder-uart-gui/blob/main/screenshots_of_UI_progress/wifitab_v0.8.png.png?raw=true)

![alt text](https://github.com/4motionEnjoyer/marauder-uart-gui/blob/main/screenshots_of_UI_progress/settingstab_v0.8.png.png?raw=true)

![alt text](https://github.com/4motionEnjoyer/marauder-uart-gui/blob/main/screenshots_of_UI_progress/manualinputtab_v0.8.png.png?raw=true)
