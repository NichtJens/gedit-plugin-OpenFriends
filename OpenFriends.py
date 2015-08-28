
from gi.repository import GObject, Gtk, Gedit, Gio

SEP_DOT = "."

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

class ExamplePlugin04(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "OpenFriendsPlugin"
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

    def _add_ui(self):
        manager = self.window.get_ui_manager()
        self._actions = Gtk.ActionGroup("OpenFriendsActions")
        self._actions.add_actions([(
            'OpenFriendsAction', Gtk.STOCK_INDEX,
            "Open _Friends", "<Ctrl><Alt>O",
            "Open the header belonging to a source, and vice versa",
            self.on_action_activate
            )])
        manager.insert_action_group(self._actions)
        self._ui_merge_id = manager.add_ui_from_string(UI_XML)
        manager.ensure_update()

    def _remove_ui(self):
        manager = self.window.get_ui_manager()
        manager.remove_ui(self._ui_merge_id)
        manager.remove_action_group(self._actions)
        manager.ensure_update()

    def do_activate(self):
        self._add_ui()

    def do_deactivate(self):
        self._remove_ui()

    def do_update_state(self):
        pass

    def on_action_activate(self, action, data=None):
        document = self.window.get_active_document()
        if not document:
            return

        location = document.get_uri_for_display()

        loc_list = location.split(SEP_DOT)
        loc_base = SEP_DOT.join(loc_list[:-1])
        loc_ext  = loc_list[-1].lower()

        friends_list  = [("c", "cxx", "cpp", "h")]
        friends_list += [("tex", "bib")]

        new_locations = []
        for friends in friends_list:
            if loc_ext in friends:
                others = [f for f in friends if f != loc_ext]
                for other_ext in others:
                    new_locations += insensitive_glob(loc_base + "." + other_ext)

        # if loc_ext.startswith("c"):
        #     new_locations = insensitive_glob(loc_base + ".h*")
        # elif loc_ext.startswith("h"):
        #     new_locations = insensitive_glob(loc_base + ".c*")
        # else:
        #     return

        if not new_locations:
            return

        for new_location in new_locations:
            new_file = Gio.file_new_for_path(new_location)

            tab = self.window.get_tab_from_location(new_file)
            if tab:
                self.window.set_active_tab(tab)
            else:
                self.window.create_tab_from_location(new_file, None, 0, 0, False, True)



import glob

def re_either(c):
    return "[{}{}]".format(c.lower(), c.upper()) if c.isalpha() else c

def insensitive_glob(pattern):
    return glob.glob("".join(re_either(c) for c in pattern))
