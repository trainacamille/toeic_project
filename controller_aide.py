import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from vue import View


class Controller(object):
    def __init__(self, model, view, identifiant):
        self._model = model
        self._view = view
		self.iden = identifiant

        self._view.connect('aide-ready', self.aide)

        self._view.show_all()

        Gtk.main()

    def aide(self, b, lettre):
        /*self._model.ajout(lettre, self.iden)*/