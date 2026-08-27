import os
import re
import shutil
import time
from pathlib import Path


def get_notes_dir() -> Path:
    notes_dir = Path.home() / "Notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    return notes_dir


def get_trash_dir() -> Path:
    trash_dir = get_notes_dir() / ".trash"
    trash_dir.mkdir(parents=True, exist_ok=True)
    return trash_dir


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-') or 'catatan'


def extract_title(content: str, default_name: str = "Catatan Tanpa Judul") -> str:
    for line in content.splitlines():
        line_str = line.strip()
        if line_str.startswith('#'):
            title = line_str.lstrip('#').strip()
            if title:
                return title
        elif line_str:
            return line_str[:30].strip()
    return default_name


def list_notes(auto_create: bool = True) -> list[dict]:
    notes_dir = get_notes_dir()
    notes = []
    
    # Ignore hidden folders like .trash
    existing_files = [f for f in notes_dir.glob("*.md") if not f.name.startswith('.')]
    if not existing_files and auto_create:
        create_note("Catatan Pertama")
        existing_files = [f for f in notes_dir.glob("*.md") if not f.name.startswith('.')]

    for filepath in existing_files:
        try:
            stat = filepath.stat()
            content = filepath.read_text(encoding='utf-8')
            title = extract_title(content, filepath.stem)
            notes.append({
                'filename': filepath.name,
                'title': title,
                'path': filepath,
                'modified': stat.st_mtime
            })
        except Exception:
            continue
    notes.sort(key=lambda x: x['modified'], reverse=True)
    return notes


def load_note(filename: str) -> str:
    filepath = get_notes_dir() / filename
    if filepath.exists():
        return filepath.read_text(encoding='utf-8')
    return ""


def save_note(filename: str, content: str) -> str:
    notes_dir = get_notes_dir()
    title = extract_title(content)
    base_slug = slugify(title)
    
    current_filepath = notes_dir / filename if filename else None
    
    # Target filename based on title slug
    new_filename = f"{base_slug}.md"
    target_filepath = notes_dir / new_filename
    
    # Avoid collision with another file if title changed
    counter = 1
    while target_filepath.exists() and (current_filepath is None or target_filepath != current_filepath):
        new_filename = f"{base_slug}-{counter}.md"
        target_filepath = notes_dir / new_filename
        counter += 1
        
    if current_filepath and current_filepath.exists() and current_filepath != target_filepath:
        current_filepath.unlink()
        
    target_filepath.write_text(content, encoding='utf-8')
    return target_filepath.name


def create_note(title: str = "Catatan Baru") -> str:
    notes_dir = get_notes_dir()
    content = f"# {title}\n\nTulis catatan di sini...\n"
    base_slug = slugify(title)
    filename = f"{base_slug}.md"
    filepath = notes_dir / filename
    
    counter = 1
    while filepath.exists():
        filename = f"{base_slug}-{counter}.md"
        filepath = notes_dir / filename
        counter += 1
        
    filepath.write_text(content, encoding='utf-8')
    return filename


def delete_note(filename: str) -> str | None:
    filepath = get_notes_dir() / filename
    if filepath.exists():
        trash_dir = get_trash_dir()
        trash_filepath = trash_dir / filename
        shutil.move(str(filepath), str(trash_filepath))
        return filename
    return None


def restore_note(filename: str) -> bool:
    trash_filepath = get_trash_dir() / filename
    if trash_filepath.exists():
        target_filepath = get_notes_dir() / filename
        shutil.move(str(trash_filepath), str(target_filepath))
        return True
    return False
