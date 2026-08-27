# NoteItDown

Aplikasi catatan pendamping (companion notebook) desktop berbasis GTK 4 dan Python 3 untuk sistem operasi Arch Linux dan Linux desktop.

---

## Fitur Utama

- **Penyimpanan Format Markdown**: Semua catatan disimpan secara otomatis dalam format `.md` standar di direktori `~/Notes`.
- **Mode Ringkas & Panel Samping (Sidebar)**: Ukuran jendela hemat ruang (~460x680 px) dengan panel daftar catatan yang dapat disembunyikan.
- **Tampilan Split-View Real-Time**: Editor teks mentah bersampingan langsung dengan pratinjau Markdown terformat (Judul H1-H3, Teks Tebal, Miring, Kode, Daftar Poin, dan Kutipan).
- **Mode Always-On-Top**: Jendela dapat disematkan di atas jendela aplikasi lain (kompatibel dengan KDE Plasma, GNOME, X11, dan Wayland).
- **Pintas Keyboard (Shortcuts)**: Dukungan penuh tombol pintas untuk efisiensi navigasi (`Ctrl+N`, `Ctrl+F`, `Ctrl+P`, `Ctrl+S`, `Ctrl+D`, `Ctrl+Shift+S`).
- **Bilah Alat Format Teks**: Tombol format cepat untuk memasukkan sintaks Markdown secara instan.
- **Autosave dan Statistik Penulisan**: Indikator status penyimpanan otomatis serta penghitung jumlah kata dan karakter real-time.
- **Sistem Sampah dan Pembatalan (Undo)**: Penghapusan aman yang memindahkan berkas ke direktori sampah tersembunyi dengan fitur pembatalan penghapusan.
- **Pengalihan Tema Gelap dan Terang**: Pengalihan tema tampilan secara langsung melalui integrasi setelan GTK Application.
- **Salin Teks Bersih**: Fitur satu klik untuk menyalin isi catatan ke clipboard sistem.

---

## Prasyarat Sistem (Arch Linux)

Instal dependensi sistem yang diperlukan melalui manajer paket `pacman`:

```bash
sudo pacman -S python-gobject gtk4 libadwaita wmctrl xdotool
```

Untuk sistem berbasis Debian atau Ubuntu:

```bash
sudo apt update
sudo apt install python3-gi libgtk-4-dev wmctrl xdotool
```

---

## Panduan Penggunaan

1. **Kloning Repositori**:
   ```bash
   git clone https://github.com/USERNAME/NoteItDown.git
   cd NoteItDown
   ```

2. **Jalankan Aplikasi**:
   ```bash
   python3 main.py
   ```

---

## Tabel Pintas Keyboard

| Kombinasi Tombol | Fungsi |
| --- | --- |
| `Ctrl + N` | Membuat catatan baru |
| `Ctrl + F` | Fokus ke kolom pencarian catatan |
| `Ctrl + P` | Mengaktifkan atau mematikan mode Always-on-Top |
| `Ctrl + S` | Menyimpan catatan secara manual |
| `Ctrl + D` | Menghapus catatan yang sedang aktif |
| `Ctrl + Shift + S` | Menampilkan atau menyembunyikan panel samping |

---

## Pengujian Otomatis

Jalankan pengujian unit otomatis menggunakan modul `unittest`:

```bash
python3 -m unittest discover -p "test_*.py"
```

---

## Struktur Repositori

- `main.py`: Titik masuk utama aplikasi (`Gtk.Application`).
- `notebook_window.py`: Jendela utama antarmuka pengguna, bilah alat, dan penanganan pintas keyboard.
- `markdown_renderer.py`: Modul pemroses dan pemformat pratinjau Markdown menggunakan Pango TextTag.
- `storage.py`: Modul manajemen berkas catatan Markdown (`~/Notes`) dan direktori sampah (`.trash`).
- `test_storage.py`: Berkas pengujian unit untuk fungsi manajemen berkas.
- `test_markdown_renderer.py`: Berkas pengujian unit untuk modul pemformat Markdown.
- `requirements.txt`: Spesifikasi dependensi Python.
- `.gitignore`: Aturan pengabaian berkas sistem dan cache Git.
- `README.md`: Dokumentasi utama proyek (Bahasa Indonesia).
- `README.en.md`: Dokumentasi proyek (Bahasa Inggris).

---

## Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT.
