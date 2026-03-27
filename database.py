import sqlite3
import os
from pathlib import Path
from typing import Dict, List


DEFAULT_DB_PATH = Path(__file__).resolve().parent / "portfolio.db"
DB_PATH = Path(os.getenv("DATABASE_PATH", str(DEFAULT_DB_PATH)))


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def save_contact(data: Dict[str, str]) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO contacts (name, email, message)
            VALUES (?, ?, ?)
            """,
            (data["name"], data["email"], data["message"]),
        )
        conn.commit()
        return int(cursor.lastrowid)


def get_contacts() -> List[Dict[str, str]]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, name, email, message, created_at
            FROM contacts
            ORDER BY id DESC
            """
        ).fetchall()

    return [dict(row) for row in rows]
