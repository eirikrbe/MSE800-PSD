import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "car_rental.db"))

class DatabaseManager:
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
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cars (
                    car_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vin TEXT NOT NULL UNIQUE,
                    make TEXT NOT NULL,
                    model TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    mileage INTEGER NOT NULL,
                    daily_rate REAL NOT NULL,
                    status TEXT NOT NULL CHECK(status IN ('locked', 'rented', 'available')) DEFAULT 'available',
                    min_rent_period INTEGER NOT NULL,
                    max_rent_period INTEGER NOT NULL,
                    total_booking_attempts INTEGER NOT NULL DEFAULT 0,
                    total_conflicts INTEGER NOT NULL DEFAULT 0
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bookings (
                    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER NOT NULL,
                    car_id INTEGER NOT NULL,
                    start_date TEXT NOT NULL,
                    end_date TEXT NOT NULL,
                    total_fee REAL NOT NULL,
                    status TEXT NOT NULL CHECK(status IN ('pending', 'approved', 'active', 'rejected', 'cancelled', 'completed')) DEFAULT 'pending',
                    FOREIGN KEY (customer_id) REFERENCES users(user_id),
                    FOREIGN KEY (car_id) REFERENCES cars(car_id)
                )
            """)
            connection.commit()
            print("Tables created successfully.")
        except sqlite3.Error as e:
            raise Exception(f"Error creating tables: {e}")

# General method to execute queries with error handling

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


