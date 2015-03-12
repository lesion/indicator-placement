#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Copyright © 2015 Rocco De Patto <rocco.depatto@gmail.com>
#
# This file is part of indicator-placement.
#
# indicator-placement is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# indicator-placement is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# indicator-placement.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, GLib
from gi.repository import AppIndicator3 as appindicator

import os.path
import locale
from locale import gettext as _
import subprocess
import json
from time import sleep
from X import display, get_windows, get_desktop, get_geometry, get_class, set_desktop, moveresize

from os.path import expanduser

class Placement:

    def __init__(self,disp):
        self.disp=disp
        self.ind = appindicator.Indicator.new(' Placement',
                'indicator-placement',
                appindicator.IndicatorCategory.APPLICATION_STATUS)

        # Delete/modify the following file when distributing as a package

        self.ind.set_icon_theme_path(os.path.abspath(os.path.join(os.path.dirname(__file__),
                'Icons')))
        self.ind.set_icon_full('emblem-default', 'Placement Indicator')
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.ind.set_title(_('Placement'))

        # Create Menu

        self.menu = Gtk.Menu()

        self.mLoadSession = Gtk.MenuItem(_('Load Session'))
        self.menu.append(self.mLoadSession)
        self.mLoadSession.connect('activate', self.loadSession, None)
        self.mLoadSession.show()

        s = Gtk.SeparatorMenuItem.new()
        self.menu.append(s)
        s.show()

        self.mSaveSession = Gtk.MenuItem(_('Save Session'))
        self.menu.append(self.mSaveSession)
        self.mSaveSession.connect('activate', self.saveSession, None)
        self.mSaveSession.show()

        self.mQuit = Gtk.MenuItem(_('Quit'))
        self.menu.append(self.mQuit)
        self.mQuit.connect('activate', Gtk.main_quit, None)
        self.mQuit.show()

        # Connect Indicator to menu

        self.ind.set_menu(self.menu)


    def getSession(self):
        windows = []
        for win in get_windows(self.disp):
            workspace = get_desktop(self.disp, win)

            if workspace == 0xffffffff: continue
            name = get_class(self.disp,win)
            windows.append({
                    'id': win,
                    'workspace': workspace,
                    'geometry': get_geometry(self.disp,win),
                    'name': "%s.%s" % (name[0],name[1])
                })
        return windows

    def loadConfig(self):
        home = expanduser('~')
        with open(os.path.join(home, '.placement.json'), 'r') as f:
            config = json.load(f)
            f.close()
        return config

    def restoreWin(self, win, config):

        # searching for win in config
        print (win)
        found = False

        for win_data in config:
            if win_data['name'] != win['name']: continue
            found=True
            break

        if not found: return

        # move to correct desktop
        print( "Move win %s to workspace %d" % (win['name'],win_data['workspace']))
        set_desktop(self.disp,win['id'],win_data['workspace'])

        sleep(0.05)
        # resize
        moveresize(self.disp,win['id'],
                    win_data['geometry'][0],
                    win_data['geometry'][1],
                    win_data['geometry'][2],
                    win_data['geometry'][3],10)
        sleep(.05)


    def loadSession(self, *args):

        # parse .placement.json

        config = self.loadConfig()

        # get current windows info (placement/size)

        curr_windows = self.getSession()

        # for each current window, search for it in placement.json
        # and restore size/position/desktop if needed

        for win in curr_windows:
            self.restoreWin(win, config)

    def saveSession(self, *args):
        curr_windows = self.getSession()
        home = expanduser('~')
        print (curr_windows)
        with open(os.path.join(home, '.placement.json'), 'w') as f:
            json.dump(curr_windows, f)
        f.close()


def main():
    try:
        locale.setlocale(locale.LC_ALL, '')
    except:
        locale.setlocale(locale.LC_ALL, 'C')

    # If we're running from /usr, then .mo files are not in MO_DIR.

    if os.path.abspath(__file__)[:4] == '/usr':

        # Fallback to default

        locale_dir = None
    else:
        locale_dir = os.path.join(os.path.dirname(__file__), 'po')
    locale.bindtextdomain('Placement', locale_dir)
    locale.textdomain('Placement')


    indicator = Placement(display.Display())
    Gtk.main()


if __name__ == '__main__':
    main()
