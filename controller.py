from gi.repository import Gtk
from vue import View
from model import Model
import gi
gi.require_version('Gtk', '3.0')

class Controller:
    def __init__(self):
        self.model = Model()
        view = View()

    def printear(self, b):
        print(self.model.data)
