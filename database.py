import sqlite3
import json
from models import Note

class DatabaseManager:
    def __init__(self, db_path="notes.db"):
        self.db_path = db_path
        self._create_table()

    def _get_connection(self):
        # check_same_thread=False allows the AI agent to access the DB safely
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _create_table(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    tags TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def add_note(self, title: str, content: str, tags: list) -> int:
        tags_json = json.dumps(tags)
        with self._get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO notes (title, content, tags) VALUES (?, ?, ?)",
                (title, content, tags_json)
            )
            return cursor.lastrowid

    def search_notes(self, query: str = None, tag: str = None):
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            sql = "SELECT * FROM notes WHERE 1=1"
            params = []
            if query:
                sql += " AND (title LIKE ? OR content LIKE ?)"
                params.extend([f"%{query}%", f"%{query}%"])
            if tag:
                sql += " AND tags LIKE ?"
                params.append(f"%{tag}%")
            cursor.execute(sql, params)
            return [dict(row) for row in cursor.fetchall()]

    def update_note(self, note_id: int, title: str = None, content: str = None, tags: list = None):
        updates, params = [], []
        if title: updates.append("title = ?"); params.append(title)
        if content: updates.append("content = ?"); params.append(content)
        if tags: updates.append("tags = ?"); params.append(json.dumps(tags))
        if not updates: return False
        params.append(note_id)
        with self._get_connection() as conn:
            cursor = conn.execute(f"UPDATE notes SET {', '.join(updates)} WHERE id = ?", params)
            return cursor.rowcount > 0

    def delete_note(self, note_id: int):
        with self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            return cursor.rowcount > 0