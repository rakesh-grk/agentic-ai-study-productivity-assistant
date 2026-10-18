import sqlite3
import re
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
from core.configuration import AppConfig
from core.models import MemoryRecord

class MemoryManager:
    """Manages persistent SQLite storage for user-approved task summaries and preferences.
    
    Adheres strictly to privacy standards: never stores API keys or raw tokens.
    """
    
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or AppConfig.DB_PATH
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        """Initializes tables using safe parameterized DDL."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS task_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    goal TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    tags TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    details_json TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_preferences (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            conn.commit()

    def _sanitize(self, text: str) -> str:
        """Strips out accidental API keys or secrets before persisting."""
        # Redact patterns resembling API keys (e.g. sk-..., AIza...)
        sanitized = re.sub(r"sk-[a-zA-Z0-9]{20,}", "[REDACTED_KEY]", text)
        sanitized = re.sub(r"AIza[0-9A-Za-z-_]{35}", "[REDACTED_KEY]", sanitized)
        return sanitized

    def save_task_memory(self, goal: str, summary: str, tags: str = "general", details: Optional[Dict[str, Any]] = None) -> int:
        """Saves an approved task record to persistent memory using parameterized SQL."""
        safe_goal = self._sanitize(goal.strip())
        safe_summary = self._sanitize(summary.strip())
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        details_str = self._sanitize(json.dumps(details or {}, ensure_ascii=False))

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO task_memory (goal, summary, tags, created_at, details_json) VALUES (?, ?, ?, ?, ?)",
                (safe_goal, safe_summary, tags, now_str, details_str)
            )
            conn.commit()
            return cursor.lastrowid

    def get_all_memories(self, limit: int = 50) -> List[MemoryRecord]:
        """Retrieves past approved tasks ordered by latest first."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, goal, summary, tags, created_at, details_json FROM task_memory ORDER BY id DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            return [
                MemoryRecord(
                    id=row["id"],
                    goal=row["goal"],
                    summary=row["summary"],
                    tags=row["tags"],
                    created_at=row["created_at"],
                    details_json=row["details_json"]
                ) for row in rows
            ]

    def search_memories(self, query: str) -> List[MemoryRecord]:
        """Performs parameterized search across past goals and summaries."""
        param = f"%{query.strip()}%"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, goal, summary, tags, created_at, details_json FROM task_memory WHERE goal LIKE ? OR summary LIKE ? ORDER BY id DESC",
                (param, param)
            )
            rows = cursor.fetchall()
            return [
                MemoryRecord(
                    id=row["id"],
                    goal=row["goal"],
                    summary=row["summary"],
                    tags=row["tags"],
                    created_at=row["created_at"],
                    details_json=row["details_json"]
                ) for row in rows
            ]

    def delete_memory(self, memory_id: int) -> bool:
        """Deletes a specific memory record by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM task_memory WHERE id = ?", (memory_id,))
            conn.commit()
            return cursor.rowcount > 0

    def clear_all_memories(self) -> bool:
        """Clears all stored task records."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM task_memory")
            conn.commit()
            return True

    def set_preference(self, key: str, value: str) -> None:
        """Persists a user preference."""
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user_preferences (key, value, updated_at) VALUES (?, ?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at",
                (key, value, now_str)
            )
            conn.commit()

    def get_preference(self, key: str, default: str = "") -> str:
        """Retrieves a stored user preference."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM user_preferences WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row["value"] if row else default
