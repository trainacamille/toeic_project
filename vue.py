import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Gdk
import os


#definition de la vue
class View(Gtk.Window):

	#definition des signaux qui seront emis
    __gsignals__={
        'telecharg-ready': (GObject.SIGNAL_RUN_FIRST, None,(str,)),
        'correct-clicked': (GObject.SIGNAL_RUN_FIRST, None,(str,str,)),
        'display-clicked': (GObject.SIGNAL_RUN_FIRST, None,(str,)),
        'enr-clicked': (GObject.SIGNAL_RUN_FIRST, None,(str,)),
    }

	#definition de initialisation de la vue
    def __init__(self):
		#initialisation de la fenetre
        Gtk.Window.__init__(self, title="logiciel Toeic")
        self.set_border_width(10)
        self.resize(600,500)

		#ajout du css a la fenetre
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
			window{
                background: url("qccm.png") no-repeat;
                background-size:cover;
                font-family:georgia, serif;
			}
		""")

        self.get_style_context().add_provider(css_provider,600)
        """Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)"""

		#ajout boite verticale
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL , spacing=6)
        self.add(vbox)

		#ajout de la barre d'onglets
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.NONE)
        stack.set_transition_duration(1000)

		#ajout des grilles pour les onglets
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


		#ajout des elements de l'onglet telechargement
        self.sel_tel = Gtk.FileChooserButton("Selectionner un dossier")
        self.sel_tel.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
        but= Gtk.Button(label="Valider")

        stack.add_titled(gr, "tel", "Telecharger")

        but.connect("clicked",self.tel)

        gr.attach(self.sel_tel,0,0,1,2)
        gr.attach(but,0,2,1,2)

		#ajout des elements de l'onglet enregistrer correction
        button1 = Gtk.Button(label="Commencer l'enregistrement")
        self.entry1 = Gtk.Entry()
        self.entry1.set_placeholder_text("Nom du TOEIC")

        grid.attach(self.entry1,0,0,1,2)
        grid.attach(button1,0,3,1,2)

        stack.add_titled(grid, "enr", "Enregistrer correction")

        button1.connect("clicked",self.enrg_corr)

		#ajout des elements de l'onglet correction
        self.sel_cor = Gtk.FileChooserButton("Selectionner un dossier")
        self.sel_cor.set_action(Gtk.FileChooserAction.SELECT_FOLDER)

        button2 = Gtk.Button(label="Lancer la correction")
        self.button3 = Gtk.Button(label="Afficher resultats")
        self.button3.set_sensitive(False)

        self.box = Gtk.ComboBoxText()
        for i in os.listdir('JSON'):
            name=i.split(".")
            self.box.append_text(name[0])
		

        grid2.attach(self.box, 0, 0, 5, 1)
        grid2.attach(self.sel_cor, 6,0, 5, 1)
        grid2.attach(button2, 3, 3, 5, 1)
        grid2.attach(self.button3, 3, 4, 5, 1)

        stack.add_titled(grid2, "cor", "Corriger")

        button2.connect("clicked",self.correct)
        self.button3.connect("clicked",self.display)

		#ajout de l'echangeur des onglets
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        vbox.pack_start(stack_switcher, False , False, 0)
        vbox.pack_start(stack, True, False, 0)

	#fonction pour le clic du bouton telecharger
    def tel(self,b):
        self.emit('telecharg-ready', self.sel_tel.get_filename())

	#fonction pour le clic du bouton commencer l'enregistrement
    def enrg_corr(self,b):
        self.emit('enr-clicked', self.entry1.get_text())
        self.box.append_text(self.entry1.get_text())
		
	#fonction pour le clic du bouton corriger
    def correct(self,b):
        self.emit('correct-clicked',self.box.get_active_text(),self.sel_cor.get_filename())

	#fonction pour le clic du bouton afficher
    def display(self,b):
        self.emit('display-clicked',self.sel_cor.get_filename())
