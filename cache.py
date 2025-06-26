import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "entity_cache.db")

def init_cache():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS entity_cache (group_key TEXT PRIMARY KEY, peer_id TEXT)"
        )

def get_peer_id_from_cache(group_key: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT peer_id FROM entity_cache WHERE group_key = ?", (group_key,))
        row = cursor.fetchone()
        return row[0] if row else None

def save_peer_id_to_cache(group_key: str, peer_id: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO entity_cache (group_key, peer_id) VALUES (?, ?)",
            (group_key, peer_id)
        )
