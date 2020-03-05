import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Gdk, GdkPixbuf



class View(Gtk.Window):

    __gsignals__={
        'telecharg-ready': (GObject.SIGNAL_RUN_FIRST, None,(str,)),
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

        self.choix_1 =Gtk.RadioButton(label="Reponse 1")
        self.choix_2 = Gtk.RadioButton.new_with_label_from_widget(self.choix_1,"Reponse 2")
        self.choix_3 = Gtk.RadioButton.new_with_label_from_widget(self.choix_1,"Reponse 3")
        self.choix_4 = Gtk.RadioButton.new_with_label_from_widget(self.choix_1,"Reponse 4")

        but= Gtk.Button(label="Valider")


        but.connect("clicked",self.send)

        gr.attach(self.choix_1,0,0,1,1)
        gr.attach(self.choix_2,1,0,1,1)
        gr.attach(self.choix_3,2,0,1,1)
        gr.attach(self.choix_4,3,0,1,1)
        gr.attach(but,1,2,2,2)

        self.connect("destroy",Gtk.main_quit)


    def send(self,b):
        self.emit('telecharg-ready', self.sel_tel.get_filename())

win = View("qccm.png")
win.show_all()
Gtk.main()
