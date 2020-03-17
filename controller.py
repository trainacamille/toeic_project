import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from vue import View



class Controller(object):
    def __init__(self, model, view):
        self._model = model
        self._view = view

        self._view.connect('telecharg-ready', self.tel)
        self._view.connect('correct-clicked', self.correct)
        self._view.connect('display-clicked', self.display)
        self._view.connect('enr-clicked', self.enrg_corr)
        self._view.connect("destroy", Gtk.main_quit)

        self._view.show_all()

        Gtk.main()

    def enrg_corr(self, b, nom):
        self._model.enregist(nom)

    def correct(self, b, nom, path):
        print("correction")

    def display(self, b):
        print("affichage")

    def tel(self, b, path):
        self._model.telecharger(path)
