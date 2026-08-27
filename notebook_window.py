import os
import subprocess
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
from gi.repository import Gtk, Gdk, GLib, Pango
import storage
from markdown_renderer import MarkdownRenderer


class NotebookWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title("NoteItDown")
        self.set_default_size(460, 680)

        self.current_filename = None
        self.auto_save_timeout_id = None
        self.always_on_top = False
        self.last_deleted_filename = None

        self._build_ui()
        self._setup_shortcuts()
        self.refresh_notes_list()

    def _build_ui(self):
        # ---------------- HEADER BAR ----------------
        self.header_bar = Gtk.HeaderBar()
        self.set_titlebar(self.header_bar)

        # New Note Button
        self.btn_new = Gtk.Button(icon_name="document-new-symbolic")
        self.btn_new.set_tooltip_text("Catatan Baru (Ctrl+N)")
        self.btn_new.connect("clicked", self.on_new_note_clicked)
        self.header_bar.pack_start(self.btn_new)

        # Toggle Sidebar Button
        self.btn_sidebar = Gtk.ToggleButton(icon_name="sidebar-show-symbolic")
        self.btn_sidebar.set_active(True)
        self.btn_sidebar.set_tooltip_text("Tampilkan/Sembunyikan Panel Catatan (Ctrl+Shift+S)")
        self.btn_sidebar.connect("toggled", self.on_sidebar_toggled)
        self.header_bar.pack_start(self.btn_sidebar)

        # Copy Text Button
        self.btn_copy = Gtk.Button(icon_name="edit-copy-symbolic")
        self.btn_copy.set_tooltip_text("Salin Teks Catatan ke Clipboard")
        self.btn_copy.connect("clicked", self.on_copy_text_clicked)
        self.header_bar.pack_end(self.btn_copy)

        # Theme Switcher Toggle (Dark / Light Mode)
        self.btn_theme = Gtk.ToggleButton(icon_name="weather-clear-night-symbolic")
        self.btn_theme.set_tooltip_text("Toggle Mode Gelap / Terang")
        self.btn_theme.connect("toggled", self.on_theme_toggled)
        self.header_bar.pack_end(self.btn_theme)

        # Toggle Always on Top Button
        self.btn_pin = Gtk.ToggleButton(icon_name="window-pin-symbolic")
        self.btn_pin.set_tooltip_text("Selalu di Atas (Ctrl+P)")
        self.btn_pin.connect("toggled", self.on_pin_toggled)
        self.header_bar.pack_end(self.btn_pin)

        # Toggle Split View Button
        self.btn_split = Gtk.ToggleButton(icon_name="view-dual-symbolic")
        self.btn_split.set_active(True)
        self.btn_split.set_tooltip_text("Toggle Live Preview (Split View)")
        self.btn_split.connect("toggled", self.on_split_toggled)
        self.header_bar.pack_end(self.btn_split)

        # Top Vertical Container (Window Child)
        self.root_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(self.root_box)

        # ---------------- UNDO BANNER (INFOBAR) ----------------
        self.undo_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.undo_box.set_margin_top(4)
        self.undo_box.set_margin_bottom(4)
        self.undo_box.set_margin_start(8)
        self.undo_box.set_margin_end(8)
        self.undo_box.set_visible(False)

        self.lbl_undo_msg = Gtk.Label(label="Catatan telah dihapus.", xalign=0)
        self.lbl_undo_msg.set_hexpand(True)
        self.undo_box.append(self.lbl_undo_msg)

        self.btn_undo = Gtk.Button(label="Batalkan (Undo)")
        self.btn_undo.connect("clicked", self.on_undo_clicked)
        self.undo_box.append(self.btn_undo)

        self.root_box.append(self.undo_box)

        # ---------------- MAIN PANED LAYOUT ----------------
        self.main_paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        self.main_paned.set_vexpand(True)
        self.root_box.append(self.main_paned)

        # ---------------- SIDEBAR ----------------
        self.sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.sidebar_box.set_size_request(160, -1)
        self.sidebar_box.set_margin_top(6)
        self.sidebar_box.set_margin_bottom(6)
        self.sidebar_box.set_margin_start(6)
        self.sidebar_box.set_margin_end(6)

        # Search Bar
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text("Cari catatan... (Ctrl+F)")
        self.search_entry.connect("search-changed", self.on_search_changed)
        self.sidebar_box.append(self.search_entry)

        # ListBox inside ScrolledWindow
        self.notes_listbox = Gtk.ListBox()
        self.notes_listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.notes_listbox.connect("row-selected", self.on_note_selected)

        scroll_sidebar = Gtk.ScrolledWindow()
        scroll_sidebar.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll_sidebar.set_vexpand(True)
        scroll_sidebar.set_child(self.notes_listbox)
        self.sidebar_box.append(scroll_sidebar)

        self.main_paned.set_start_child(self.sidebar_box)

        # ---------------- EDITOR & PREVIEW CONTAINER ----------------
        self.right_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.main_paned.set_end_child(self.right_container)

        # Formatting Toolbar above Editor
        self.fmt_toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        self.fmt_toolbar.set_margin_top(4)
        self.fmt_toolbar.set_margin_bottom(4)
        self.fmt_toolbar.set_margin_start(6)
        self.fmt_toolbar.set_margin_end(6)
        self._build_formatting_toolbar()
        self.right_container.append(self.fmt_toolbar)

        # Split-View Paned (Editor | Preview)
        self.editor_paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        self.editor_paned.set_vexpand(True)
        self.right_container.append(self.editor_paned)

        # Raw Markdown Editor
        self.editor_view = Gtk.TextView()
        self.editor_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.editor_view.set_margin_top(6)
        self.editor_view.set_margin_bottom(6)
        self.editor_view.set_margin_start(6)
        self.editor_view.set_margin_end(6)
        self.editor_buffer = self.editor_view.get_buffer()
        self.editor_buffer.connect("changed", self.on_editor_changed)

        scroll_editor = Gtk.ScrolledWindow()
        scroll_editor.set_hexpand(True)
        scroll_editor.set_vexpand(True)
        scroll_editor.set_child(self.editor_view)
        self.editor_paned.set_start_child(scroll_editor)

        # Live Markdown Preview
        self.preview_view = Gtk.TextView()
        self.preview_view.set_editable(False)
        self.preview_view.set_cursor_visible(False)
        self.preview_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.preview_view.set_margin_top(6)
        self.preview_view.set_margin_bottom(6)
        self.preview_view.set_margin_start(6)
        self.preview_view.set_margin_end(6)
        self.preview_buffer = self.preview_view.get_buffer()
        self.markdown_renderer = MarkdownRenderer(self.preview_buffer)

        scroll_preview = Gtk.ScrolledWindow()
        scroll_preview.set_hexpand(True)
        scroll_preview.set_vexpand(True)
        scroll_preview.set_child(self.preview_view)
        self.editor_paned.set_end_child(scroll_preview)

        # ---------------- FOOTER STATUS BAR ----------------
        self.footer_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        self.footer_box.set_margin_top(4)
        self.footer_box.set_margin_bottom(4)
        self.footer_box.set_margin_start(10)
        self.footer_box.set_margin_end(10)

        # Status Autosave Label
        self.lbl_status = Gtk.Label(label="● Tersimpan", xalign=0)
        self.lbl_status.set_hexpand(True)
        self.footer_box.append(self.lbl_status)

        # Word & Character Counter
        self.lbl_stats = Gtk.Label(label="0 kata | 0 karakter", xalign=1)
        self.footer_box.append(self.lbl_stats)

        self.root_box.append(self.footer_box)

    def _build_formatting_toolbar(self):
        buttons = [
            ("format-text-bold-symbolic", "Tebal (**teks**)", lambda b: self.insert_formatting("**", "**")),
            ("format-text-italic-symbolic", "Miring (*teks*)", lambda b: self.insert_formatting("*", "*")),
            ("heading1", "Heading 1 (# )", lambda b: self.insert_prefix("# ")),
            ("heading2", "Heading 2 (## )", lambda b: self.insert_prefix("## ")),
            ("format-list-bullet-symbolic", "Daftar Poin (- )", lambda b: self.insert_prefix("- ")),
            ("code-symbolic", "Kode (`kode`)", lambda b: self.insert_formatting("`", "`")),
            ("quote-symbolic", "Kutipan (> )", lambda b: self.insert_prefix("> ")),
        ]

        for icon_or_label, tooltip, callback in buttons:
            if icon_or_label.startswith("heading"):
                btn = Gtk.Button(label=icon_or_label.upper())
            else:
                btn = Gtk.Button(icon_name=icon_or_label)
            btn.set_tooltip_text(tooltip)
            btn.set_has_frame(False)
            btn.connect("clicked", callback)
            self.fmt_toolbar.append(btn)

    def _setup_shortcuts(self):
        controller = Gtk.EventControllerKey()
        controller.connect("key-pressed", self.on_key_pressed)
        self.add_controller(controller)

    def on_key_pressed(self, controller, keyval, keycode, state):
        ctrl = bool(state & Gdk.ModifierType.CONTROL_MASK)
        shift = bool(state & Gdk.ModifierType.SHIFT_MASK)

        if ctrl and not shift:
            if keyval in (Gdk.KEY_n, Gdk.KEY_N):
                self.on_new_note_clicked(None)
                return True
            elif keyval in (Gdk.KEY_f, Gdk.KEY_F):
                self.search_entry.grab_focus()
                return True
            elif keyval in (Gdk.KEY_p, Gdk.KEY_P):
                self.btn_pin.set_active(not self.btn_pin.get_active())
                return True
            elif keyval in (Gdk.KEY_s, Gdk.KEY_S):
                self.force_save()
                return True
            elif keyval in (Gdk.KEY_d, Gdk.KEY_D):
                if self.current_filename:
                    self.on_delete_note_clicked(None, self.current_filename)
                return True
        elif ctrl and shift:
            if keyval in (Gdk.KEY_s, Gdk.KEY_S):
                self.btn_sidebar.set_active(not self.btn_sidebar.get_active())
                return True

        return False

    def insert_formatting(self, prefix: str, suffix: str):
        buf = self.editor_buffer
        if buf.get_has_selection():
            _, start, end = buf.get_selection_bounds()
            text = buf.get_text(start, end, True)
            buf.delete(start, end)
            buf.insert(start, f"{prefix}{text}{suffix}")
        else:
            iter_pos = buf.get_iter_at_mark(buf.get_insert())
            buf.insert(iter_pos, f"{prefix}teks{suffix}")
        self.editor_view.grab_focus()

    def insert_prefix(self, prefix: str):
        buf = self.editor_buffer
        iter_pos = buf.get_iter_at_mark(buf.get_insert())
        line_num = iter_pos.get_line()
        _, line_start = buf.get_iter_at_line(line_num)
        buf.insert(line_start, prefix)
        self.editor_view.grab_focus()

    def refresh_notes_list(self, filter_query: str = ""):
        while True:
            row = self.notes_listbox.get_row_at_index(0)
            if row is None:
                break
            self.notes_listbox.remove(row)

        notes = storage.list_notes()
        filter_query = filter_query.lower().strip()

        target_row = None
        for n in notes:
            if filter_query and filter_query not in n['title'].lower():
                continue

            row = Gtk.ListBoxRow()
            row.filename = n['filename']

            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            box.set_margin_top(4)
            box.set_margin_bottom(4)
            box.set_margin_start(6)
            box.set_margin_end(6)

            lbl = Gtk.Label(label=n['title'], xalign=0)
            lbl.set_ellipsize(Pango.EllipsizeMode.END)
            lbl.set_hexpand(True)
            box.append(lbl)

            btn_del = Gtk.Button(icon_name="user-trash-symbolic")
            btn_del.set_has_frame(False)
            btn_del.set_tooltip_text("Hapus Catatan (Ctrl+D)")
            btn_del.connect("clicked", self.on_delete_note_clicked, n['filename'])
            box.append(btn_del)

            row.set_child(box)
            self.notes_listbox.append(row)

            if self.current_filename and n['filename'] == self.current_filename:
                target_row = row

        if target_row:
            self.notes_listbox.select_row(target_row)
        elif self.notes_listbox.get_row_at_index(0):
            first_row = self.notes_listbox.get_row_at_index(0)
            self.notes_listbox.select_row(first_row)
        else:
            self.current_filename = None
            self.editor_buffer.set_text("")
            self.preview_buffer.set_text("")
            self._update_stats("")

    def on_note_selected(self, listbox, row):
        if row is None:
            return
        filename = getattr(row, 'filename', None)
        if not filename or filename == self.current_filename:
            return

        self.current_filename = filename
        content = storage.load_note(filename)

        self.editor_buffer.handler_block_by_func(self.on_editor_changed)
        self.editor_buffer.set_text(content)
        self.editor_buffer.handler_unblock_by_func(self.on_editor_changed)

        self.markdown_renderer.render(content)
        self._update_stats(content)
        self.lbl_status.set_label("● Tersimpan")

    def on_editor_changed(self, buffer):
        text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), True)
        self.markdown_renderer.render(text)
        self._update_stats(text)
        self.lbl_status.set_label("○ Menyimpan...")

        if self.auto_save_timeout_id:
            GLib.source_remove(self.auto_save_timeout_id)
        self.auto_save_timeout_id = GLib.timeout_add(500, self._do_auto_save)

    def _update_stats(self, text: str):
        words = len(text.split())
        chars = len(text)
        self.lbl_stats.set_label(f"{words} kata | {chars} karakter")

    def _do_auto_save(self):
        self.auto_save_timeout_id = None
        if not self.current_filename:
            return False

        text = self.editor_buffer.get_text(
            self.editor_buffer.get_start_iter(),
            self.editor_buffer.get_end_iter(),
            True
        )
        new_filename = storage.save_note(self.current_filename, text)
        if new_filename != self.current_filename:
            self.current_filename = new_filename
            self.refresh_notes_list()
            
        self.lbl_status.set_label("● Tersimpan")
        return False

    def force_save(self):
        if self.auto_save_timeout_id:
            GLib.source_remove(self.auto_save_timeout_id)
        self._do_auto_save()

    def on_new_note_clicked(self, button):
        new_filename = storage.create_note("Catatan Baru")
        self.current_filename = new_filename
        self.refresh_notes_list()
        self.editor_view.grab_focus()

    def on_delete_note_clicked(self, button, filename):
        deleted = storage.delete_note(filename)
        if deleted:
            self.last_deleted_filename = filename
            self.lbl_undo_msg.set_label(f"Catatan '{filename}' telah dihapus.")
            self.undo_box.set_visible(True)

            if self.current_filename == filename:
                self.current_filename = None
            self.refresh_notes_list()

    def on_undo_clicked(self, button):
        if self.last_deleted_filename:
            if storage.restore_note(self.last_deleted_filename):
                self.current_filename = self.last_deleted_filename
                self.refresh_notes_list()
            self.last_deleted_filename = None
        self.undo_box.set_visible(False)

    def on_copy_text_clicked(self, button):
        text = self.editor_buffer.get_text(
            self.editor_buffer.get_start_iter(),
            self.editor_buffer.get_end_iter(),
            True
        )
        clipboard = Gdk.Display.get_default().get_clipboard()
        clipboard.set(text)
        self.lbl_status.set_label("✓ Tersalin ke clipboard!")
        GLib.timeout_add(2000, lambda: self.lbl_status.set_label("● Tersimpan") or False)

    def on_theme_toggled(self, button):
        is_dark = button.get_active()
        settings = Gtk.Settings.get_default()
        if settings:
            settings.set_property("gtk-application-prefer-dark-theme", is_dark)

    def on_search_changed(self, entry):
        query = entry.get_text()
        self.refresh_notes_list(query)

    def on_sidebar_toggled(self, button):
        show = button.get_active()
        self.sidebar_box.set_visible(show)

    def on_split_toggled(self, button):
        show = button.get_active()
        self.editor_paned.get_end_child().set_visible(show)

    def on_pin_toggled(self, button):
        self.always_on_top = button.get_active()
        try:
            if self.always_on_top:
                subprocess.run(["wmctrl", "-r", "NoteItDown", "-b", "add,above"], check=False)
                subprocess.run(["xdotool", "search", "--onlyvisible", "--name", "NoteItDown", "windowactivate", "windowraise"], check=False)
            else:
                subprocess.run(["wmctrl", "-r", "NoteItDown", "-b", "remove,above"], check=False)
        except Exception:
            pass
