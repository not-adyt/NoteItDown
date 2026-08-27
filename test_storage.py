import unittest
import os
import shutil
import tempfile
from pathlib import Path
import storage


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_get_notes_dir = storage.get_notes_dir
        storage.get_notes_dir = lambda: Path(self.test_dir)

    def tearDown(self):
        storage.get_notes_dir = self.original_get_notes_dir
        shutil.rmtree(self.test_dir)

    def test_create_and_load_note(self):
        filename = storage.create_note("Proyek Arch Linux")
        self.assertTrue(filename.endswith(".md"))
        
        content = storage.load_note(filename)
        self.assertIn("# Proyek Arch Linux", content)

    def test_list_notes(self):
        storage.create_note("Catatan Pertama")
        storage.create_note("Catatan Kedua")
        notes = storage.list_notes()
        self.assertEqual(len(notes), 2)
        titles = [n['title'] for n in notes]
        self.assertIn("Catatan Pertama", titles)
        self.assertIn("Catatan Kedua", titles)

    def test_save_and_update_note(self):
        filename = storage.create_note("Beli Kopi")
        new_content = "# Beli Kopi Espresso\n\n- Arabica 200g\n"
        updated_filename = storage.save_note(filename, new_content)
        
        content = storage.load_note(updated_filename)
        self.assertEqual(content, new_content)

    def test_delete_and_restore_note(self):
        filename = storage.create_note("Catatan Sementara")
        deleted_file = storage.delete_note(filename)
        self.assertEqual(deleted_file, filename)
        
        notes = storage.list_notes(auto_create=False)
        self.assertEqual(len(notes), 0)

        # Restore note from trash
        self.assertTrue(storage.restore_note(filename))
        notes_after_restore = storage.list_notes(auto_create=False)
        self.assertEqual(len(notes_after_restore), 1)
        self.assertEqual(notes_after_restore[0]['filename'], filename)


if __name__ == "__main__":
    unittest.main()
