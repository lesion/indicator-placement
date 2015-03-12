#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Xlib.protocol.event import ClientMessage
from Xlib import X, display


def send_event(disp, win, data, event_type, mask,):
    event = ClientMessage(window=win, client_type=event_type,
                          data=(32, data))
    return disp.screen().root.send_event(event, event_mask=mask)


def get_property(disp, name):
    atom = disp.intern_atom(name)
    return disp.screen().root.get_full_property(atom, 0)


def get_window_property(disp, name, window):
    atom = disp.intern_atom(name)

    return disp.create_resource_object('window',
                                       window).get_full_property(atom, 0)


def get_property_value(disp, name):
    return get_property(disp, name).value[0]


def get_window_property_value(disp, name, window):
    return get_window_property(disp, name, window).value[0]

def moveresize(disp, window, x=-1,y=-1,w=-1,h=-1, grav=0):
    event_type = disp.intern_atom('_NET_MOVERESIZE_WINDOW')
    mask = X.SubstructureRedirectMask | X.SubstructureNotifyMask
    grflags = grav;
    if x != -1: grflags |= (1 << 8)
    if y != -1: grflags |= (1 << 9)
    if w != -1: grflags |= (1 << 10)
    if h != -1: grflags |= (1 << 11)
    data = [grflags, max(x, 0), max(y, 0), max(w, 0), max(h, 0)]
    return send_event(disp, window, data, event_type, mask)

# send window to another desktop
def set_desktop(disp, window, desktop):
    event_type = disp.intern_atom('_NET_WM_DESKTOP')
    mask = X.PropertyChangeMask
    data = [desktop, 0, 0, 0, 0]
    return send_event(disp, window, data, event_type, mask)

# which desktop is window on
def get_desktop(disp, window):
    return get_window_property_value(disp, '_NET_WM_DESKTOP', window)

def set_active_window(disp, window):
    event_type = disp.intern_atom('_NET_ACTIVE_WINDOW')
    mask = X.PropertyChangeMask
    data = [0, 0, 0, 0, 0]
    return send_event(disp, window, data, event_type, mask)

def get_active_window(disp):
    return get_property_value(disp, '_NET_ACTIVE_WINDOW')

def get_number_of_desktops(disp):
    return get_property_value(disp, '_NET_NUMBER_OF_DESKTOPS')

def get_current_desktop(disp):
    return get_property_value(disp, '_NET_CURRENT_DESKTOP')
# also
#get_property_value(disp, '_WIN_WORKSPACE')
def set_current_desktop(disp, desktop):
    event_type = disp.intern_atom('_NET_CURRENT_DESKTOP')
    mask = X.SubstructureRedirectMask | X.SubstructureNotifyMask
    data = [desktop, 0, 0, 0, 0]
    return send_event(disp, disp.screen().root, data, event_type, mask)

def get_pid(disp, window):
    return get_window_property_value(disp, '_NET_WM_PID', window)

def get_windows(disp):
    return get_property(disp, '_NET_CLIENT_LIST').value

def get_geometry(disp, window):
    w = disp.create_resource_object('window', window)
    w.map()
    g = w.get_geometry()
    t = g.root.translate_coords(w, g.x, g.y)
    return ( t.x-g.x, t.y-g.y, g.width, g.height)#,t.x,t.y)

def get_class(disp,window):
    w = disp.create_resource_object('window', window)
    return w.get_wm_class()


