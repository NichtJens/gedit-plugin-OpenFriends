
NAME      = "OpenFriends"
MENULABEL = "Open _Friends"
TOOLTIP   = "Open the header belonging to a source, and vice versa"
SHORTCUT  = "<Ctrl><Alt>O"

SEP_DOT = "."
FRIENDSHIPS  = [("c", "cxx", "cpp", "h")]
#FRIENDSHIPS += [("tex", "bib")]

UI_XML = """
<ui>
  <menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
      <placeholder name="ToolsOps">
        <menuitem name="OpenFriendsAction" action="OpenFriendsAction"/>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""



from gi.repository import GObject, Gtk, Gedit, Gio

class OpenFriendsPlugin(GObject.Object, Gedit.WindowActivatable):

    __gtype_name__ = NAME + "Plugin"
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        self._add_ui()

    def do_deactivate(self):
        self._remove_ui()

    def do_update_state(self):
        pass


    def _add_ui(self):
        action = Gtk.Action(NAME + "Action", MENULABEL, TOOLTIP, Gtk.STOCK_INDEX)
        action.connect("activate", self.on_action_activate)

        self._actions = Gtk.ActionGroup(NAME + "Actions")
        self._actions.add_action_with_accel(action, SHORTCUT)

        manager = self.window.get_ui_manager()
        manager.insert_action_group(self._actions)
        self._ui_merge_id = manager.add_ui_from_string(UI_XML)
        manager.ensure_update()


    def _remove_ui(self):
        manager = self.window.get_ui_manager()
        manager.remove_ui(self._ui_merge_id)
        manager.remove_action_group(self._actions)
        manager.ensure_update()


    def on_action_activate(self, action, data=None):
        document = self.window.get_active_document()
        if not document:
            return

        location = document.get_uri_for_display()
        loc_base, loc_ext = split_location(location)

        new_locations = []
        for clique in FRIENDSHIPS:
            if loc_ext in clique:
                others = (f for f in clique if f != loc_ext)
                for other_ext in others:
                    new_locations += insensitive_glob(loc_base + SEP_DOT + other_ext)

        # if loc_ext.startswith("c"):
        #     new_locations = insensitive_glob(loc_base + ".h*")
        # elif loc_ext.startswith("h"):
        #     new_locations = insensitive_glob(loc_base + ".c*")
        # else:
        #     return

        if not new_locations:
            return

        for new_loc in new_locations:
            self._open_tab(new_loc)


    def _open_tab(self, location):
        gfile = Gio.file_new_for_path(location)

        tab = self.window.get_tab_from_location(gfile)
        if tab:
            self.window.set_active_tab(tab)
        else:
            self.window.create_tab_from_location(gfile, None, 0, 0, False, True)



def split_location(location):
    loc_list = location.split(SEP_DOT)
    base = SEP_DOT.join(loc_list[:-1])
    ext  = loc_list[-1].lower()
    return base, ext



import glob

def re_either(c):
    return "[{}{}]".format(c.lower(), c.upper()) if c.isalpha() else c

def insensitive_glob(pattern):
    return glob.glob("".join(re_either(c) for c in pattern))


