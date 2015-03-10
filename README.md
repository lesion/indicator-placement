# poswin
Remember windows desktop/position/size for Linux WM / gnome / kde / gala 

## WARNING!! THIS IS AN ALPHA RELEASE !!

## What poswin does?
It simply remember windows position/size on linux wm

## Why?
Because there's no way to do it!!
See this bug on launchpad for more details:
https://bugs.launchpad.net/ubuntu/+source/metacity/+bug/124315

and a lot of people arguing:
http://askubuntu.com/questions/8834/how-do-i-save-remember-last-used-window-position-and-size-for-applications (the solution here is, never shutdown your computer, hibernate!)

http://ubuntuforums.org/showthread.php?t=1173410


## How it works?
I'm using [wmctrl](http://en.wikipedia.org/wiki/Wmctrl) to retrieve and restore windows placement and size on desktop.

I've started this little script reading [this blog entry](http://movingtofreedom.org/2010/08/10/arranging-windows-from-the-gnulinux-command-line-with-wmctrl/)

## How to use

After cloning it and install npm dependencies:

`chmod +x poswin.js`
`./poswin.js save`

this will create a ~/.poswin.json

to reload position:

`./poswin.js load`


