# utils/db.py
import sqlite3
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

BASE = Path(__file__).resolve().parent.parent
DB_PATH = BASE / "candidates.db"

def get_conn():
    return sqlite3.connect(str(DB_PATH))

def init_db() -> None:
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            headline TEXT,
            profile_json TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_candidate(name: str, headline: str, profile: Dict[str, Any]) -> int:
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO candidates (name, headline, profile_json) VALUES (?, ?, ?)",
        (name, headline, json.dumps(profile, ensure_ascii=False))
    )
    conn.commit()
    rowid = c.lastrowid
    conn.close()
    return rowid

def update_candidate(id: int, name: Optional[str], headline: Optional[str], profile: Optional[Dict[str, Any]]):
    conn = get_conn()
    c = conn.cursor()
    if name is not None:
        c.execute("UPDATE candidates SET name=? WHERE id=?", (name, id))
    if headline is not None:
        c.execute("UPDATE candidates SET headline=? WHERE id=?", (headline, id))
    if profile is not None:
        c.execute("UPDATE candidates SET profile_json=? WHERE id=?", (json.dumps(profile, ensure_ascii=False), id))
    conn.commit()
    conn.close()

def get_candidate_by_name(name: str) -> Optional[Dict[str, Any]]:
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, name, headline, profile_json FROM candidates WHERE name = ?", (name,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    return {"id": row[0], "name": row[1], "headline": row[2], "profile": json.loads(row[3])}

def get_candidate_by_id(id: int) -> Optional[Dict[str, Any]]:
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, name, headline, profile_json FROM candidates WHERE id = ?", (id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    return {"id": row[0], "name": row[1], "headline": row[2], "profile": json.loads(row[3])}

def list_candidates(limit: int = 1000) -> List[str]:
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT name FROM candidates ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return [r[0] for r in rows]

def bulk_insert_candidates(profiles: List[Dict[str, Any]]) -> int:
    """
    profiles: list of dicts containing keys: name, headline, profile (raw json-like)
    """
    conn = get_conn()
    c = conn.cursor()
    count = 0
    for p in profiles:
        name = p.get("name")
        headline = p.get("headline", "")
        profile = p.get("profile", p)
        c.execute("INSERT INTO candidates (name, headline, profile_json) VALUES (?, ?, ?)",
                  (name, headline, json.dumps(profile, ensure_ascii=False)))
        count += 1
    conn.commit()
    conn.close()
    return count
