import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,GObject





class VueFormulaireDeCorrection(Gtk.Window):
    __gsignals__={
        'validation-ready': (GObject.SIGNAL_RUN_FIRST, None,(GObject.TYPE_PYOBJECT,)),
    }

    def __init__(self,titre):

        #boxfenetre boite de stockage de tous les elements de la fenetre
        boxfenetre = Gtk.HBox(homogeneous=False,spacing=15)
        #hbox = boites de questions, vbox = boites de colonnes, button= tableau de RadioButton
        hbox = []
        vbox = []
        button = []
        Gtk.Window.__init__(self, title=titre)
        self.maximize()
        #construction des boites de questions


        for i in range(200) :
             hbox.append(Gtk.HBox(homogeneous=False,spacing=0))
        # construction des colonnes de questions

        for i in range(8) :
            vbox.append(Gtk.VBox(homogeneous=False,spacing=0))
        # construction des boutons radios pour chaque question et insersion dans les boites de questions
        #j indice des boites de questions
        j = 0
        # k indice pour la numerotation des questions
        k = 1
        for i in range(800):
            if i%4 == 0:
                # creation nouvelle ligne de questions et ajout des signaux au boutton
                button.append(Gtk.RadioButton.new_with_label_from_widget(None, "A"))
                button[i].connect("toggled", self.on_button_toggled, i )
                hbox[j].pack_start(Gtk.Label(str(k)), True, True, 10)
                hbox[j].pack_start(button[i], True, True, 0)
                k = k+ 1
            elif i%4 == 1 :
                # création case B et ajout à la boite existante
                button.append(Gtk.RadioButton.new_with_label_from_widget(button[i-1], "B"))
                button[i].connect("toggled", self.on_button_toggled, i)
                hbox[j].pack_start(button[i], True, True, 0)
            elif i%4 == 2:
                # création case C et ajout à la boite existante
                button.append( Gtk.RadioButton.new_with_label_from_widget(button[i-2], "C"))
                button[i].connect("toggled", self.on_button_toggled, i)
                hbox[j].pack_start(button[i], True, True, 0)
            else :
                # création case D et ajout à la boite existante
                button.append(Gtk.RadioButton.new_with_label_from_widget(button[i-3], "D"))
                button[i].connect("toggled", self.on_button_toggled, i)
                hbox[j].pack_start(button[i], True , True, 0)
                j = j+1
        # insersion des boites questions dans les colonnes
        j = 0 # j indice pour la colonne
        i = 0 # i indice pour la ligne de question
        for i in range(200):

            if i%25 < 24 :
                vbox[j].pack_start(hbox[i],False,False,0)
            else :
                vbox[j].pack_start(hbox[i],False,False,0)
                j= j+1
        #insersion des colonnes dans la boite principale

        i = 0 # i indice des colonnes de questions
        for i in range(8) :
                boxfenetre.pack_start(vbox[i], False, False, 0)

        valider = Gtk.Button(label="Valider")
        valider.connect("clicked", self.on_button_clicked,button)
        boxfenetre.pack_start(valider, False, False, 0)
        self.add(boxfenetre)


    #fonction de verification d'activation du bouton
    def on_button_toggled(self, button, name):
        if button.get_active():
            state = "okey"
        else:
            state = "off"


    #fonction validation de la grille
    def on_button_clicked(self,widget, button):

        self.emit("validation-ready",button)
