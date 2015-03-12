# indicator-placement
Remember windows desktop/position/size for Linux WM / gnome / kde / gala 

## WARNING!! THIS IS AN ALPHA RELEASE !!

## What indicator-placement does?
It simply remember windows position/size on linux wm

## Why?
Because there's no other way to do it!!
See this bug on launchpad for more details:
https://bugs.launchpad.net/ubuntu/+source/metacity/+bug/124315

and a lot of people arguing:
http://askubuntu.com/questions/8834/how-do-i-save-remember-last-used-window-position-and-size-for-applications (suggested solution here is, never shutdown your computer, hibernate !?!?!)

http://ubuntuforums.org/showthread.php?t=1173410


## How it works?
I'm using python3-xlib to retrieve and restore windows placement and size on desktop, so you need to install it with `apt-get install python3-xlib`.


## How to use

After cloning it and install python3-xlib, run
`./indicator-placement.py` , click on the indicator:

1. Save session will store all windows placement (workspace, x/y and width/height)

2. Load session will restore all windows placement (workspace, x/y and width/height)

## TODO
 - Fullscreen windows aren't working!!!

