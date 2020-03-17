import Model_vue_formulaire as m
import Vue_formulaire as v
import Controleur_vue_formulaire as c

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio



class Application(Gtk.Application):

    def __init__(self,nom_fichier):
        self.fichier = nom_fichier
        application_id="a.b12"
        flags = Gio.ApplicationFlags.FLAGS_NONE

        super(Application, self).__init__(flags=flags,application_id = application_id)

    def do_activate(self):
        #Argument de la vee a changer par ce qui est envoye par le controleur principale
        c.Controleur_vue_formulaireCorrection(m.Model(),v.VueFormulaireDeCorrection(self.fichier))

    def do_startup(self):

        Gtk.Application.do_startup(self)
