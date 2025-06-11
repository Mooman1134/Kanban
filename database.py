import os
import sqlite3
from datetime import datetime

DB_FILE = os.environ.get('DB_FILE', 'cards.db')


def connect():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with connect() as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                set_name TEXT NOT NULL
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                card_id INTEGER NOT NULL,
                price REAL NOT NULL,
                fetched_at TEXT NOT NULL,
                FOREIGN KEY(card_id) REFERENCES cards(id)
            )
            """
        )
        db.commit()


def get_or_create_card(name: str, set_name: str) -> int:
    with connect() as db:
        cur = db.execute(
            "SELECT id FROM cards WHERE name = ? AND set_name = ?",
            (name, set_name),
        )
        row = cur.fetchone()
        if row:
            return row["id"]
        cur = db.execute(
            "INSERT INTO cards(name, set_name) VALUES (?, ?)",
            (name, set_name),
        )
        db.commit()
        return cur.lastrowid


def add_price(card_id: int, price: float):
    with connect() as db:
        db.execute(
            "INSERT INTO prices(card_id, price, fetched_at) VALUES (?, ?, ?)",
            (card_id, price, datetime.utcnow().isoformat()),
        )
        db.commit()


def get_latest_prices():
    with connect() as db:
        cur = db.execute(
            """
            SELECT c.id, c.name, c.set_name, p.price, p.fetched_at
            FROM cards c
            JOIN (
                SELECT card_id, price, MAX(fetched_at) AS fetched_at
                FROM prices
                GROUP BY card_id
            ) p ON c.id = p.card_id
            ORDER BY c.name
            """
        )
        return [dict(row) for row in cur.fetchall()]


def get_price_history(card_id: int):
    with connect() as db:
        cur = db.execute(
            "SELECT price, fetched_at FROM prices WHERE card_id = ? ORDER BY fetched_at",
            (card_id,),
        )
        return [dict(row) for row in cur.fetchall()]
