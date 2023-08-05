Cloud Connector Python
-----------------------------
Created by Idop - 21.6.2016

reads Modbuc TCP \ EtherNetIP \ Simulation  tags and send to web service using OAuth authentication
Runs on Python 2.7.9 and tested on raspberi Pi3 - debian Jesi OS

How to Operate:
------------------------------
After installing correctly all componenets you can run
sudo python CI_CloudConnector.py help
This will show all operating options

after testing is done you can operate application in production mode using

sudo python CI_CloudConnector.py MainLoop


Install Instructions
------------------------------
Project is uploaded to Open source directory "PIP"
run the next command to download and install the module

sudo pip install CI_CloudConnector

Trouble shotting
------------------------
ERROR: if pyhot.h missing run
Soultion: sudo apt-get install python-dev

ERROR: : error message when upgrading 'module object has no attribute _handlerList'
Soultion: run 'sudo pip uninstall logging' 

 
running the application 
-------------------------------
run the module from where it was deployed with help option to see instructions
importent: in the first run a config file will be created in /CI_LC/config.ini you must edit this file with server defenitions  
sudo python CI_LocalConnector.py help

* dependencies should be installed automaticly (required modules : pip , pymodbus , cpppo

running the apllication at startup (linux)
----------------------------------------
edit startupscript
sudo nano /etc/init.d/idopStartUp.sh
sudo chmod 755 /etc/init.d/idopStartUp.sh
sudo update-rc.d idopStartUp.sh defaults

to remove from startup
sudo update-rc.d -f idopStartUp.sh remove



inside this file we just call another shell
idopStartUp.sh

-------------
#! /bin/sh

# /etc/init.d/idopStartUp.sh

bash /home/pi/CI_Projects/launcher.sh &



#!/bin/sh

# launcher.sh

#navigate home than to this directory then back home


cd /

cd /home/pi/CI_Projects
export PATH="$PATH:/usr/lib/python2.7:/usr/lib/python2.7/plat-arm-linux-gnueabihf:/usr/lib/python2.7/lib-tk:/usr/lib/python2.7/lib-old:/usr/lib/python2.7/lib-dynload:/home/pi/.local/lib/python2.7/site-packages:/usr/local/lib/python2.7/dist-packages:/usr/lib/python2.7/dist-packages:/usr/lib/python2.7/dist-packages/PILcompat:/usr/lib/python2.7/dist-packages/gtk-2.0:/usr/lib/pymodules/python2.7"

sudo python CI_LocalConnector.py MainLoop


cd /