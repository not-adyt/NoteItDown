# NoteItDown 📝

A lightweight, compact desktop Markdown companion notebook application for Arch Linux & Linux desktops built with **Python 3** and **GTK 4**.

---

## ✨ Features

- 📑 **Markdown Storage**: Automatically saves notes as standard `.md` files inside `~/Notes`.
- 📌 **Compact / Sidebar Companion Mode**: Lightweight sidebar form factor (default size ~460x680 px) with collapsible note list.
- 👁️ **Live Split-View Preview**: Real-time rendered Markdown preview (Headings H1-H3, Bold, Italic, Code, Bullet Lists, Blockquotes) side-by-side with raw editing.
- 📌 **Always-On-Top Toggle**: Pin the window on top of all other windows (compatible with KDE Plasma, GNOME, X11, Wayland).
- ⌨️ **Keyboard Shortcuts**: Complete hotkey support (`Ctrl+N`, `Ctrl+F`, `Ctrl+P`, `Ctrl+S`, `Ctrl+D`, `Ctrl+Shift+S`).
- ✍️ **Formatting Toolbar**: One-click formatting buttons for quick Markdown syntax insertion.
- ⏱️ **Autosave & Statistics**: Live autosave indicator and word/character counter.
- 🗑️ **Trash Bin & Undo**: Safe soft delete with instant Undo restore.
- 🌙 **Dark & Light Mode**: Theme toggle via GTK Application settings.
- 📋 **Copy to Clipboard**: Quick copy clean note text directly to system clipboard.

---

## 🛠️ Prerequisites (Arch Linux)

Install the required system packages using `pacman`:

```bash
sudo pacman -S python-gobject gtk4 libadwaita wmctrl xdotool
```

*For Debian / Ubuntu:*
```bash
sudo apt update
sudo apt install python3-gi libgtk-4-dev wmctrl xdotool
```

---

## 🚀 Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/NoteItDown.git
   cd NoteItDown
   ```

2. **Run the application**:
   ```bash
   python3 main.py
   ```

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
| --- | --- |
| `Ctrl + N` | Create a new note |
| `Ctrl + F` | Focus search bar |
| `Ctrl + P` | Toggle Always-on-Top |
| `Ctrl + S` | Force instant save |
| `Ctrl + D` | Delete current note |
| `Ctrl + Shift + S` | Toggle Sidebar visibility |

---

## 🧪 Testing

Run the automated test suite:

```bash
python3 -m unittest discover -p "test_*.py"
```

---

## 📁 Repository Structure

```
NoteItDown/
├── main.py                   # App entry point (Gtk.Application)
├── notebook_window.py        # Main GTK4 Companion Window UI & Shortcuts
├── markdown_renderer.py      # Live Pango Tag Markdown Renderer
├── storage.py                # Markdown Note File Manager (~/Notes)
├── test_storage.py           # Unit tests for storage CRUD & trash
├── test_markdown_renderer.py # Unit tests for Markdown parser
├── requirements.txt          # Python dependency specifications
├── .gitignore                # Git ignore rules
└── README.md                 # Project documentation
```

---

## 📄 License

[MIT License](LICENSE)
