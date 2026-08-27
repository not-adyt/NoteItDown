# NoteItDown

A desktop Markdown companion notebook application for Arch Linux and Linux desktop environments, built using **Python 3** and **GTK 4**.

---

## Key Features

- **Markdown File Storage**: All notes are automatically saved as standard `.md` files in the `~/Notes` directory.
- **Compact & Sidebar Mode**: Space-saving sidebar form factor (~460x680 px) with a collapsible note list panel.
- **Real-Time Split-View**: Side-by-side raw Markdown editor and rendered preview (H1-H3 Headings, Bold, Italic, Code, Bullet Lists, and Blockquotes).
- **Always-On-Top Mode**: Pin the window on top of other desktop windows (compatible with KDE Plasma, GNOME, X11, and Wayland).
- **Keyboard Shortcuts**: Complete hotkey support for optimal efficiency (`Ctrl+N`, `Ctrl+F`, `Ctrl+P`, `Ctrl+S`, `Ctrl+D`, `Ctrl+Shift+S`).
- **Formatting Toolbar**: Quick action buttons to insert Markdown syntax without manual typing.
- **Autosave & Writing Statistics**: Real-time autosave status indicator alongside word and character count metrics.
- **Trash Bin & Undo**: Soft delete mechanism moving files to a hidden `.trash` directory with instant restoration capability.
- **Dark & Light Mode**: Theme switching integration via GTK Application settings.
- **Clean Text Copying**: One-click clipboard copy function for current note content.

---

## System Prerequisites (Arch Linux)

Install required system packages using `pacman`:

```bash
sudo pacman -S python-gobject gtk4 libadwaita wmctrl xdotool
```

For Debian or Ubuntu systems:

```bash
sudo apt update
sudo apt install python3-gi libgtk-4-dev wmctrl xdotool
```

---

## Usage Guide

1. **Clone Repository**:
   ```bash
   git clone https://github.com/USERNAME/NoteItDown.git
   cd NoteItDown
   ```

2. **Launch Application**:
   ```bash
   python3 main.py
   ```

---

## Keyboard Shortcuts Table

| Key Combination | Action |
| --- | --- |
| `Ctrl + N` | Create a new note |
| `Ctrl + F` | Focus search entry |
| `Ctrl + P` | Toggle Always-on-Top mode |
| `Ctrl + S` | Force manual save |
| `Ctrl + D` | Delete active note |
| `Ctrl + Shift + S` | Toggle sidebar visibility |

---

## Automated Testing

Run automated unit tests using the standard `unittest` framework:

```bash
python3 -m unittest discover -p "test_*.py"
```

---

## Repository Structure

- `main.py`: Application entry point (`Gtk.Application`).
- `notebook_window.py`: Primary user interface window, toolbars, and shortcut event controllers.
- `markdown_renderer.py`: Markdown parsing and preview rendering engine using Pango TextTags.
- `storage.py`: Note file management module (`~/Notes`) and trash handling (`.trash`).
- `test_storage.py`: Unit tests for storage operations.
- `test_markdown_renderer.py`: Unit tests for Markdown rendering.
- `requirements.txt`: Python dependency declarations.
- `.gitignore`: Git exclusion rules.
- `README.md`: Primary documentation (Bahasa Indonesia).
- `README.en.md`: Secondary documentation (English).

---

## License

This project is licensed under the MIT License.
