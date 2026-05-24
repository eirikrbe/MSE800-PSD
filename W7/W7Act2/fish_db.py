import os
import sqlite3


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "aquarium.db")


def connect_database(db_path=DB_PATH):
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row
    return connection


def create_tables(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS fish (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            quantity INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES category(id)
        )
        """
    )
    connection.commit()


def seed_categories(connection):
    cursor = connection.cursor()
    cursor.executemany(
        "INSERT OR IGNORE INTO category (name) VALUES (?)",
        [("Freshwater",), ("Saltwater",)],
    )
    connection.commit()


def seed_fish(connection):
    cursor = connection.cursor()
    cursor.executemany(
        """
        INSERT OR IGNORE INTO fish (name, quantity, category_id)
        VALUES (
            ?,
            ?,
            (SELECT id FROM category WHERE name = ?)
        )
        """,
        [
            ("Goldfish", 0, "Freshwater"),
            ("Angelfish", 0, "Freshwater"),
            ("Shark", 0, "Saltwater"),
            ("Tuna", 0, "Saltwater"),
            ("Salmon", 0, "Saltwater"),
        ],
    )
    connection.commit()
