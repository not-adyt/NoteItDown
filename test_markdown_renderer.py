import unittest
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
import markdown_renderer


class TestMarkdownRenderer(unittest.TestCase):

    def test_rendering(self):
        buf = Gtk.TextBuffer()
        renderer = markdown_renderer.MarkdownRenderer(buf)
        md = "# Judul\n\nIni **teks tebal** dan *miring* serta `code`.\n\n- Poin 1\n- Poin 2\n"
        renderer.render(md)
        text = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)
        self.assertIn("Judul", text)
        self.assertIn("teks tebal", text)
        self.assertIn("• Poin 1", text)


if __name__ == "__main__":
    unittest.main()
