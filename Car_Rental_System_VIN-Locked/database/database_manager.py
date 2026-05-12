import sqlite3
import os

from httpx import delete

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
    
    def create_tables(self):
        try:
            cursor = self.connection.cursor()
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
            self.connection.commit()
            print("Tables created successfully.")
        except sqlite3.Error as e:
            raise Exception(f"Error creating tables: {e}")

# General method to execute queries with error handling

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            return cursor

        except sqlite3.Error as e:
            raise Exception(f"Error executing query: {e}")
        
    def fetch_one(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchone()
        except sqlite3.Error as e:
            raise Exception(f"Error fetching one record: {e}")

    def fetch_all(self, query, params=None):
        try: 
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except sqlite3.Error as e:
            raise Exception(f"Error fetching records: {e}")

# User-related methods

    def add_user(self, full_name, email, phone, password_hash, role):
        query = """
            INSERT INTO users (full_name, email, phone, password_hash, role)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor = self.execute_query(query, (full_name, email, phone, password_hash, role))
        return cursor.lastrowid

    def get_user_by_email(self, email):
        query = "SELECT * FROM users WHERE email = ?"
        return self.fetch_one(query, (email,))

# Car-related methods

    def add_car(self, vin, make, model, year, mileage, daily_rate, min_rent_period, max_rent_period):
        query = """
            INSERT INTO cars (vin, make, model, year, mileage, daily_rate, min_rent_period, max_rent_period)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor = self.execute_query(query, (vin, make, model, year, mileage, daily_rate, min_rent_period, max_rent_period))
        return cursor.lastrowid

    def get_car_by_vin(self, vin):
        query = "SELECT * FROM cars WHERE vin = ?"
        return self.fetch_one(query, (vin,))
    
    def get_car_by_id(self, car_id):
        query = "SELECT * FROM cars WHERE car_id = ?"
        return self.fetch_one(query, (car_id,))
    
    def get_all_cars(self):
        query = "SELECT * FROM cars"
        return self.fetch_all(query)
    
    def update_car_status(self, car_id, new_status):
        allowed_statuses = ['locked', 'rented', 'available']
        if new_status not in allowed_statuses:
            raise ValueError(f"Invalid status: {new_status}. Allowed statuses are: {allowed_statuses}")
        query = "UPDATE cars SET status = ? WHERE car_id = ?"
        self.execute_query(query, (new_status, car_id))
        return True
    
    def update_car(self, car_id, make=None, model=None, year=None, mileage=None, daily_rate=None, min_rent_period=None, max_rent_period=None):
        fields = []
        params = []
        if make is not None:
            fields.append("make = ?")
            params.append(make)
        if model is not None:
            fields.append("model = ?")
            params.append(model)
        if year is not None:
            fields.append("year = ?")
            params.append(year)
        if mileage is not None:
            current_car = self.get_car_by_id(car_id)
            if current_car is None:
                raise ValueError(f"Car with ID {car_id} does not exist.")
            if mileage < current_car["mileage"]:
                raise ValueError(f"New mileage {mileage} cannot be less than current mileage {current_car['mileage']}.")
            fields.append("mileage = ?")
            params.append(mileage)
        if daily_rate is not None:
            fields.append("daily_rate = ?")
            params.append(daily_rate)
        if min_rent_period is not None:
            fields.append("min_rent_period = ?")
            params.append(min_rent_period)
        if max_rent_period is not None:
            fields.append("max_rent_period = ?")
            params.append(max_rent_period)

        if not fields:
            raise ValueError("No fields to update.")

        params.append(car_id)
        query = f"UPDATE cars SET {', '.join(fields)} WHERE car_id = ?"
        self.execute_query(query, tuple(params))
        return True
    
    def delete_car(self, car_id):
        query = "DELETE FROM cars WHERE car_id = ?"
        self.execute_query(query, (car_id,))
        return True

if __name__ == "__main__":
    db = DatabaseManager()
    '''
    # Test car insertion2
    car_id = db.add_car(
        vin="test2vin123456789",
        make="TestMake2",
        model="testmodel2",
        year=2020,
        mileage=15000,
        daily_rate=49.99,
        min_rent_period=1,
        max_rent_period=30
    )
    print(f"Inserted car with ID: {car_id}")
    
  
    db.update_car_status(car_id, "locked")
    car = db.get_car_by_id(car_id)
    print(f"Updated car status: {car['status']}")

    db.update_car(car_id, mileage=16000, daily_rate=59.99)
    car = db.get_car_by_id(car_id)
    print(f"Updated car mileage: {car['mileage']}, daily rate: {car['daily_rate']}")

    db.update_car(car_id, mileage=14000)
    '''
    car_id = 4
    db.delete_car(car_id)
    deleted_car = db.get_car_by_id(car_id)

    if deleted_car is None:
        print("Car successfully deleted.")
    else:        
        print("Car deletion failed.")

    db.disconnect()