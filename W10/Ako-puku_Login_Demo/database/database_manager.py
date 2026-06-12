import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "login_signup.db"))

class DatabaseManager:
    """Manages sqlite connection lifecycle, schema creation and simple query helpers."""
    def __init__(self):
        self.connection = None
        self.connect()
        self.create_tables()

    def connect(self):
        try:
            self.connection = sqlite3.connect(DB_PATH)
            self.connection.execute("PRAGMA foreign_keys = ON")
            self.connection.row_factory = sqlite3.Row
            print("Database connection established.")
        except sqlite3.Error as e:
            raise Exception(f"Error connecting to database: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print("Database connection closed.")

    def get_connection(self):
        if self.connection is None:
            raise ConnectionError("Database connection is not active. Call connect() first.")
        return self.connection

    def create_tables(self):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    phone TEXT,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('customer', 'admin')),
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.commit()
            print("Tables created successfully.")
        except sqlite3.Error as e:
            raise Exception(f"Error creating tables: {e}")

    def execute_query(self, query, params=None):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            connection.commit()
            return cursor
        except sqlite3.Error as e:
            raise Exception(f"Error executing query: {e}")

    def fetch_one(self, query, params=None):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchone()
        except sqlite3.Error as e:
            raise Exception(f"Error fetching one record: {e}")

    def fetch_all(self, query, params=None):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except sqlite3.Error as e:
            raise Exception(f"Error fetching records: {e}")
