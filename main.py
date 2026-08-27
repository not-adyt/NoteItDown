import sys
import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk

from notebook_window import NotebookWindow


class NoteItDownApp(Gtk.Application):

    def __init__(self):
        super().__init__(
            application_id="id.noteitdown.desktop",
            flags=0
        )

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = NotebookWindow(application=self)
        win.present()


def main():
    app = NoteItDownApp()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
