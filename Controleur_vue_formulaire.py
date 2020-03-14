import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from Vue_formulaire import VueFormulaireDeCorrection



class Controleur_vue_formulaireCorrection(object) :

    def __init__(self,modelformulaire,VueFormulaireDeCorrection):

        self._model = modelformulaire
        self._vue = VueFormulaireDeCorrection
        #ajout signal emit par la vue par
        self._vue.connect("validation-ready",self.validation)
        self._vue.connect("destroy",Gtk.main_quit)
        self._vue.show_all()



        Gtk.main()
    #fonction de validation
    def validation(self,widget,button):
        #transformation du tableau de boutons en une liste de caractère
        reponse = []
        for i in range(800) :
            if button[i].get_active():
                reponse.append(button[i].get_label())
        #ecriture dans un fichier json le formulaire de correction
        self._model.ecriture_fichier(reponse,self._vue.get_title())
        Gtk.main_quit()
