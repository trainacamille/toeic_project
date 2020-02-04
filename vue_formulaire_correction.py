import cv2 
import gi
import numpy
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk



class VueFormulaireDeCorrection(Gtk.Window):

    def __init__(self):

        boxfenetre = Gtk.HBox(homogeneous=False,spacing=15)
        hbox = []
        vbox = []
        button = []
        Gtk.Window.__init__(self, title="Fenetre du formulaire de correction")
        self.maximize()
        #construction des boites de questions


        for i in range(200) :
             hbox.append(Gtk.HBox(homogeneous=False,spacing=0))
        # construction des colonnes de questions

        for i in range(8) :
            vbox.append(Gtk.VBox(homogeneous=False,spacing=0))
        # construction des boutons radios pour chaque question et insersion dans les boites de questions
        j = 0


        for i in range(800):
            if i%4 == 0:
                button.append(Gtk.RadioButton.new_with_label_from_widget(None, "A"))
                button[i].connect("toggled", self.on_button_toggled, "%i")
                hbox[j].pack_start(button[i], False, False, 0)
            elif i%4 == 1 :
                button.append(Gtk.RadioButton.new_with_label_from_widget(button[i-1], "B"))
                button[i].connect("toggled", self.on_button_toggled, "%i")
                hbox[j].pack_start(button[i], False, False, 0)
            elif i%4 == 2:
                button.append( Gtk.RadioButton.new_with_label_from_widget(button[i-2], "C"))
                button[i].connect("toggled", self.on_button_toggled, "%i")
                hbox[j].pack_start(button[i], False, False, 0)
            else :
                button.append(Gtk.RadioButton.new_with_label_from_widget(button[i-3], "D"))
                button[i].connect("toggled", self.on_button_toggled, "%i")
                hbox[j].pack_start(button[i], False, False, 0)
                j = j+1
        # insersion des boites questions dans les colonnes
        j = 0
        i = 0
        for i in range(200):
            if i%25 < 24 :
                vbox[j].pack_start(hbox[i],False,False,0)
            else :
                vbox[j].pack_start(hbox[i],False,False,0)
                j= j+1
        #insersion des colonnes dans la boite principale
        i = 0
        for i in range(8) :
                boxfenetre.pack_start(vbox[i], False, False, 0)

        self.add(boxfenetre)

    def on_button_toggled(self, button, name):
        if button.get_active():
            state = "on"
        else:
            state = "off"
        #print("Button", name, "was turned", state)

        #self.button = Gtk.Button(label="Click Here")
        #self.image = Gtk.Image.new_from_file("AnswerSheet-1.png")
        #self.button.connect("clicked", self.on_button_clicked)
        #self.add(self.button)
        #self.image.set_pixel_size(500)
        #self.add(self.image)


    def on_button_clicked(self, widget):
        print("case sauvegarde")

win = VueFormulaireDeCorrection()

win.connect("destroy",Gtk.main_quit)
win.show_all()
Gtk.main()
