import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class View(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="logiciel Toeic")
        self.set_border_width(10)
        self.resize(1000,700)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL , spacing=6)
        self.add(vbox)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.NONE)
        stack.set_transition_duration(1000)


        grid = Gtk.Grid()
        self.add(grid)

        grid2 = Gtk.Grid()
        self.add(grid2)


        sel_tel = Gtk.FileChooserButton("Selectionner un dossier",Gtk.FileChooserAction.SELECT_FOLDER)
        sel_tel.set_action(Gtk.FileChooserAction.SELECT_FOLDER)

        stack.add_titled(sel_tel, "tel", "Telecharger")

        button1 = Gtk.Button(label="Commencer l'enregistrement")
        entry1 = Gtk.Entry()
        entry1.set_text("Nom du TOEIC")

        grid.add(entry1)
        grid.add(button1)

        stack.add_titled(grid, "enr", "Enregistrer correction")


        sel_cor = Gtk.FileChooserButton("Selectionner un dossier",Gtk.FileChooserAction.SELECT_FOLDER)
        sel_cor.set_action(Gtk.FileChooserAction.SELECT_FOLDER)

        button2 = Gtk.Button(label="Lancer la correction")

        box = Gtk.ComboBox()

        grid2.attach(box, 1, 0, 2, 1)
        grid2.attach(sel_cor, 3,0, 1, 2)
        grid2.attach(button2, 1, 2, 1, 1)

        stack.add_titled(grid2, "cor", "Corriger")

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        vbox.pack_start(stack_switcher, True, True, 0)
        vbox.pack_start(stack, True, True, 0)


win = View()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
