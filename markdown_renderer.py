import re
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Pango, Gdk


class MarkdownRenderer:

    def __init__(self, text_buffer: Gtk.TextBuffer):
        self.buffer = text_buffer
        self._setup_tags()

    def _setup_tags(self):
        tag_table = self.buffer.get_tag_table()

        def add_tag(name, **kwargs):
            tag = Gtk.TextTag.new(name)
            for k, v in kwargs.items():
                tag.set_property(k, v)
            tag_table.add(tag)

        # Headings
        add_tag("h1", font="Sans Bold 18", pixels_above_lines=12, pixels_below_lines=6)
        add_tag("h2", font="Sans Bold 15", pixels_above_lines=10, pixels_below_lines=4)
        add_tag("h3", font="Sans Bold 13", pixels_above_lines=8, pixels_below_lines=4)

        # Text styles
        add_tag("bold", weight=Pango.Weight.BOLD)
        add_tag("italic", style=Pango.Style.ITALIC)
        add_tag("code", font="Monospace 10", background="#e8e8e8", foreground="#c7254e")
        add_tag("codeblock", font="Monospace 10", background="#f5f5f5", left_margin=16, right_margin=16, pixels_above_lines=4, pixels_below_lines=4)
        add_tag("quote", style=Pango.Style.ITALIC, left_margin=20, foreground="#555555")
        add_tag("bullet", left_margin=16)

    def render(self, md_text: str):
        self.buffer.set_text("")
        lines = md_text.splitlines(keepends=True)
        in_code_block = False

        for line in lines:
            stripped = line.rstrip('\r\n')
            
            # Code block toggle ```
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                start_iter = self.buffer.get_end_iter()
                self.buffer.insert(start_iter, line)
                end_iter = self.buffer.get_end_iter()
                line_num = end_iter.get_line()
                if end_iter.get_line_offset() == 0 and line_num > 0:
                    line_num -= 1
                _, line_start = self.buffer.get_iter_at_line(line_num)
                self.buffer.apply_tag_by_name("codeblock", line_start, end_iter)
                continue

            # Heading 1 (# ...)
            if stripped.startswith("# "):
                self._insert_tagged_line(stripped[2:] + "\n", "h1")
                continue

            # Heading 2 (## ...)
            if stripped.startswith("## "):
                self._insert_tagged_line(stripped[3:] + "\n", "h2")
                continue

            # Heading 3 (### ...)
            if stripped.startswith("### "):
                self._insert_tagged_line(stripped[4:] + "\n", "h3")
                continue

            # Blockquote (> ...)
            if stripped.startswith("> "):
                self._insert_inline_formatted_line(stripped[2:] + "\n", line_tags=["quote"])
                continue

            # Bullet points (- ... or * ...)
            if stripped.startswith("- ") or stripped.startswith("* "):
                bullet_line = "• " + stripped[2:] + "\n"
                self._insert_inline_formatted_line(bullet_line, line_tags=["bullet"])
                continue

            # Regular paragraph line
            self._insert_inline_formatted_line(line)

    def _insert_tagged_line(self, text: str, tag_name: str):
        start_iter = self.buffer.get_end_iter()
        self.buffer.insert(start_iter, text)
        end_iter = self.buffer.get_end_iter()
        # Move start_iter to beginning of current insertion if needed
        line_num = end_iter.get_line()
        if end_iter.get_line_offset() == 0 and line_num > 0:
            line_num -= 1
        _, line_start = self.buffer.get_iter_at_line(line_num)
        self.buffer.apply_tag_by_name(tag_name, line_start, end_iter)

    def _insert_inline_formatted_line(self, text: str, line_tags: list = None):
        line_tags = line_tags or []
        start_line_num = self.buffer.get_end_iter().get_line()
        
        # Simple inline formatting parsing (**bold**, *italic*, `code`)
        pattern = re.compile(r'(\*\*.*?\*\*|\*.*?\*|`.*?`)')
        parts = pattern.split(text)
        
        for part in parts:
            if not part:
                continue
            iter_pos = self.buffer.get_end_iter()
            if part.startswith("**") and part.endswith("**") and len(part) >= 4:
                self.buffer.insert_with_tags_by_name(iter_pos, part[2:-2], "bold")
            elif part.startswith("*") and part.endswith("*") and len(part) >= 2:
                self.buffer.insert_with_tags_by_name(iter_pos, part[1:-1], "italic")
            elif part.startswith("`") and part.endswith("`") and len(part) >= 2:
                self.buffer.insert_with_tags_by_name(iter_pos, part[1:-1], "code")
            else:
                self.buffer.insert(iter_pos, part)
                
        if line_tags:
            end_iter = self.buffer.get_end_iter()
            _, line_start = self.buffer.get_iter_at_line(start_line_num)
            for tag in line_tags:
                self.buffer.apply_tag_by_name(tag, line_start, end_iter)

