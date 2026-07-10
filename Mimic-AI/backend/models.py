"""
Database models and helpers for the chat application.
Uses raw SQLite3 for simplicity — no ORM overhead.
"""

import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'chatapp.db')


def get_db():
    """Get a database connection with row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    """Initialize database tables."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT UNIQUE NOT NULL,
            display_name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            is_online INTEGER DEFAULT 0,
            last_seen TEXT,
            ai_standin_enabled INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT DEFAULT (datetime('now')),
            is_read INTEGER DEFAULT 0,
            is_ai_generated INTEGER DEFAULT 0,
            FOREIGN KEY (sender_id) REFERENCES users(id),
            FOREIGN KEY (receiver_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS chat_exports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            contact_name TEXT NOT NULL,
            parsed_messages TEXT NOT NULL,
            message_count INTEGER DEFAULT 0,
            uploaded_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE INDEX IF NOT EXISTS idx_messages_sender ON messages(sender_id);
        CREATE INDEX IF NOT EXISTS idx_messages_receiver ON messages(receiver_id);
        CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);
        CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone_number);
    ''')

    conn.commit()
    conn.close()
    print("[OK] Database initialized successfully")


# ─── User Operations ─────────────────────────────────────────────────

def create_user(phone_number, display_name, password_hash):
    """Create a new user. Returns user dict or None if phone exists."""
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users (phone_number, display_name, password_hash) VALUES (?, ?, ?)",
            (phone_number, display_name, password_hash)
        )
        conn.commit()
        user = conn.execute(
            "SELECT id, phone_number, display_name FROM users WHERE phone_number = ?",
            (phone_number,)
        ).fetchone()
        return dict(user)
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def get_user_by_phone(phone_number):
    """Get user by phone number."""
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE phone_number = ?",
        (phone_number,)
    ).fetchone()
    conn.close()
    return dict(user) if user else None


def get_user_by_id(user_id):
    """Get user by ID."""
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()
    conn.close()
    return dict(user) if user else None


def get_all_users(exclude_id=None):
    """Get all users, optionally excluding one (the current user)."""
    conn = get_db()
    if exclude_id:
        users = conn.execute(
            "SELECT id, phone_number, display_name, is_online, last_seen, ai_standin_enabled FROM users WHERE id != ?",
            (exclude_id,)
        ).fetchall()
    else:
        users = conn.execute(
            "SELECT id, phone_number, display_name, is_online, last_seen, ai_standin_enabled FROM users"
        ).fetchall()
    conn.close()
    return [dict(u) for u in users]


def set_user_online(user_id, online=True):
    """Update user's online status."""
    conn = get_db()
    if online:
        conn.execute(
            "UPDATE users SET is_online = 1 WHERE id = ?",
            (user_id,)
        )
    else:
        conn.execute(
            "UPDATE users SET is_online = 0, last_seen = datetime('now') WHERE id = ?",
            (user_id,)
        )
    conn.commit()
    conn.close()


def toggle_ai_standin(user_id, enabled):
    """Enable or disable AI stand-in for a user."""
    conn = get_db()
    conn.execute(
        "UPDATE users SET ai_standin_enabled = ? WHERE id = ?",
        (1 if enabled else 0, user_id)
    )
    conn.commit()
    conn.close()


# ─── Message Operations ──────────────────────────────────────────────

def save_message(sender_id, receiver_id, content, is_ai_generated=False):
    """Save a message and return it as a dict."""
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO messages (sender_id, receiver_id, content, is_ai_generated) VALUES (?, ?, ?, ?)",
        (sender_id, receiver_id, content, 1 if is_ai_generated else 0)
    )
    msg = conn.execute(
        "SELECT * FROM messages WHERE id = ?",
        (cursor.lastrowid,)
    ).fetchone()
    conn.commit()
    conn.close()
    return dict(msg)


def get_chat_history(user1_id, user2_id, limit=50, offset=0):
    """Get chat history between two users."""
    conn = get_db()
    messages = conn.execute(
        """SELECT m.*, 
                  s.display_name as sender_name, 
                  r.display_name as receiver_name
           FROM messages m
           JOIN users s ON m.sender_id = s.id
           JOIN users r ON m.receiver_id = r.id
           WHERE (m.sender_id = ? AND m.receiver_id = ?) 
              OR (m.sender_id = ? AND m.receiver_id = ?)
           ORDER BY m.timestamp ASC
           LIMIT ? OFFSET ?""",
        (user1_id, user2_id, user2_id, user1_id, limit, offset)
    ).fetchall()
    conn.close()
    return [dict(m) for m in messages]


def mark_messages_read(sender_id, receiver_id):
    """Mark all messages from sender to receiver as read."""
    conn = get_db()
    conn.execute(
        "UPDATE messages SET is_read = 1 WHERE sender_id = ? AND receiver_id = ? AND is_read = 0",
        (sender_id, receiver_id)
    )
    conn.commit()
    conn.close()


def get_unread_count(sender_id, receiver_id):
    """Get count of unread messages from sender to receiver."""
    conn = get_db()
    result = conn.execute(
        "SELECT COUNT(*) as count FROM messages WHERE sender_id = ? AND receiver_id = ? AND is_read = 0",
        (sender_id, receiver_id)
    ).fetchone()
    conn.close()
    return result['count']


# ─── Chat Export Operations ───────────────────────────────────────────

def save_chat_export(user_id, contact_name, parsed_messages):
    """Save parsed WhatsApp chat export."""
    conn = get_db()
    # Delete existing export for same user-contact pair
    conn.execute(
        "DELETE FROM chat_exports WHERE user_id = ? AND contact_name = ?",
        (user_id, contact_name)
    )
    conn.execute(
        "INSERT INTO chat_exports (user_id, contact_name, parsed_messages, message_count) VALUES (?, ?, ?, ?)",
        (user_id, contact_name, json.dumps(parsed_messages), len(parsed_messages))
    )
    conn.commit()
    conn.close()


def get_chat_export(user_id, contact_name=None):
    """Get chat export for a user, optionally filtered by contact."""
    conn = get_db()
    if contact_name:
        export = conn.execute(
            "SELECT * FROM chat_exports WHERE user_id = ? AND contact_name = ?",
            (user_id, contact_name)
        ).fetchone()
    else:
        export = conn.execute(
            "SELECT * FROM chat_exports WHERE user_id = ? ORDER BY uploaded_at DESC LIMIT 1",
            (user_id,)
        ).fetchone()
    conn.close()
    if export:
        result = dict(export)
        result['parsed_messages'] = json.loads(result['parsed_messages'])
        return result
    return None


def get_all_chat_exports(user_id):
    """Get all chat exports for a user."""
    conn = get_db()
    exports = conn.execute(
        "SELECT id, user_id, contact_name, message_count, uploaded_at FROM chat_exports WHERE user_id = ?",
        (user_id,)
    ).fetchall()
    conn.close()
    return [dict(e) for e in exports]
