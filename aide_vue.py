import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Gdk, GdkPixbuf



class View(Gtk.Window):

    __gsignals__={
        'aide-ready': (GObject.SIGNAL_RUN_FIRST, None,(str,)),
    }

    def __init__(self, file):
        Gtk.Window.__init__(self, title="Probleme")
        self.set_border_width(10)
        self.resize(600,300)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL , spacing=6)
        self.add(vbox)

        pix =GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=file,width = 90, height = 50,preserve_aspect_ratio=True)

        img= Gtk.Image()
        img.set_from_pixbuf(pix)

        vbox.add(img)

        gr = Gtk.Grid()
        vbox.add(gr)
        gr.set_column_homogeneous(True)
        gr.set_row_spacing(30)

        self.choix_1 =Gtk.RadioButton(label="Reponse A")
        self.choix_2 = Gtk.RadioButton.new_with_label_from_widget(self.choix_1,"Reponse B")
        self.choix_3 = Gtk.RadioButton.new_with_label_from_widget(self.choix_1,"Reponse C")
        self.choix_4 = Gtk.RadioButton.new_with_label_from_widget(self.choix_1,"Reponse D")
        self.choix_5 = Gtk.RadioButton.new_with_label_from_widget(self.choix_1,"Aucune de ces reponses")

        but= Gtk.Button(label="Valider")


        but.connect("clicked",self.send)

        gr.attach(self.choix_1,0,0,2,1)
        gr.attach(self.choix_2,2,0,2,1)
        gr.attach(self.choix_3,4,0,2,1)
        gr.attach(self.choix_4,6,0,2,1)
        gr.attach(self.choix_5,8,0,2,1)
        gr.attach(but,3,2,4,2)

        self.connect("delete_event",self.rien)

    def send(self,b):
        self.emit('aide-ready', "ex")
        Gtk.main_quit()

    def rien(self,b,k):
        return True



#win = View("qccm.png")
#win.show_all()
#Gtk.main()
