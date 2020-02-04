import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Gdk



class View(Gtk.Window):

    __gsignals__={
        'telecharg-ready': (GObject.SIGNAL_RUN_FIRST, None,()),
        'correct-clicked': (GObject.SIGNAL_RUN_FIRST, None,()),
        'display-clicked': (GObject.SIGNAL_RUN_FIRST, None,()),
        'enr-clicked': (GObject.SIGNAL_RUN_FIRST, None,()),
    }

    def __init__(self):
        Gtk.Window.__init__(self, title="logiciel Toeic")
        self.set_border_width(10)
        self.resize(600,500)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data("""
			window{
                background: url("qccm.png") no-repeat;
                background-size:cover;
                font-family:georgia, serif;
			}
		""")

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL , spacing=6)
        self.add(vbox)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.NONE)
        stack.set_transition_duration(1000)

        gr = Gtk.Grid()
        self.add(gr)
        gr.set_column_homogeneous(True)
        gr.set_row_spacing(30)

        grid = Gtk.Grid()
        self.add(grid)
        grid.set_column_homogeneous(True)
        grid.set_row_spacing(30)


        grid2 = Gtk.Grid()
        self.add(grid2)
        grid2.set_column_homogeneous(True)
        grid2.set_row_homogeneous(True)
        grid2.set_row_spacing(30)

        sel_tel = Gtk.FileChooserButton("Selectionner un dossier")
        sel_tel.set_action(Gtk.FileChooserAction.SELECT_FOLDER)

        stack.add_titled(gr, "tel", "Telecharger")

        sel_tel.connect("file-set",self.tel)

        gr.attach(sel_tel,0,0,1,2)

        button1 = Gtk.Button(label="Commencer l'enregistrement")
        entry1 = Gtk.Entry()
        entry1.set_text("Nom du TOEIC")

        grid.attach(entry1,0,0,1,2)
        grid.attach(button1,0,3,1,2)

        stack.add_titled(grid, "enr", "Enregistrer correction")

        button1.connect("clicked",self.enrg_corr)

        sel_cor = Gtk.FileChooserButton("Selectionner un dossier")
        sel_cor.set_action(Gtk.FileChooserAction.SELECT_FOLDER)

        button2 = Gtk.Button(label="Lancer la correction")
        button3 = Gtk.Button(label="Afficher resultats")
        button3.set_sensitive(False)

        box = Gtk.ComboBox()

        grid2.attach(box, 0, 0, 5, 1)
        grid2.attach(sel_cor, 6,0, 5, 1)
        grid2.attach(button2, 3, 3, 5, 1)
        grid2.attach(button3, 3, 4, 5, 1)

        stack.add_titled(grid2, "cor", "Corriger")

        button2.connect("clicked",self.correct)
        button3.connect("clicked",self.display)

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        vbox.pack_start(stack_switcher, False , False, 0)
        vbox.pack_start(stack, True, False, 0)


    def tel(self,b):
        self.emit('telecharg-ready')

    def enrg_corr(self,b):
        self.emit('enr-clicked')

    def correct(self,b):
        self.emit('correct-clicked')

    def display(self,b):
        self.emit('display-clicked')
