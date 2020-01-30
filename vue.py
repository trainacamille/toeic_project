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

        button12 = Gtk.Button(label="Button 1")
        button22 = Gtk.Button(label="Button 2")
        button32 = Gtk.Button(label="Button 3")
        button42 = Gtk.Button(label="Button 4")
        button52 = Gtk.Button(label="Button 5")
        button62 = Gtk.Button(label="Button 6")

        grid2.add(button12)
        grid2.attach(button22, 1, 0, 2, 1)
        grid2.attach_next_to(button32, button12, Gtk.PositionType.BOTTOM, 1, 2)
        grid2.attach_next_to(button42, button32, Gtk.PositionType.RIGHT, 2, 1)
        grid2.attach(button52, 1, 2, 1, 1)
        grid2.attach_next_to(button62, button52, Gtk.PositionType.RIGHT, 1, 1)

        stack.add_titled(grid2, "cor", "Corriger")

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        vbox.pack_start(stack_switcher, True, True, 0)
        vbox.pack_start(stack, True, True, 0)


win = View()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
