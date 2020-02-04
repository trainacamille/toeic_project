import model as m
import vue as v
import controller as c

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

class Application(Gtk.Application):

    def __init__(self):

        flags = Gio.ApplicationFlags.FLAGS_NONE

        super(Application, self).__init__(flags=flags)

    def do_activate(self):
        c.Controller(m.Model(),v.View())

    def do_startup(self):
        Gtk.Application.do_startup(self)
