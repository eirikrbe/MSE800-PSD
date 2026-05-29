
import sqlite3
import sys

DB_NAME = "cars.db"

MENU = (
    "\nCar Rental System"
    "\n1. Add Car"
    "\n2. List Cars"
    "\n3. Remove Car"
    "\n4. Exit"
    "\nChoose: "
)

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS cars (
            plate TEXT PRIMARY KEY,
            car_type TEXT NOT NULL,
            year INTEGER NOT NULL CHECK(year >= 1886)
        )
        """
    )
    conn.commit()
    conn.close()

def add_car(plate, car_type, year):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO cars (plate, car_type, year) VALUES (?, ?, ?)",
            (plate.strip().upper(), car_type.strip(), int(year)),
        )
        conn.commit()
        print(f"Car {plate} added.")
    except sqlite3.IntegrityError:
        print("❌ Car with this plate already exists!")
    finally:
        conn.close()

def list_cars():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT plate, car_type, year FROM cars ORDER BY plate")
    rows = cur.fetchall()
    conn.close()
    if not rows:
        print("(no cars found)")
        return
    print("\nPlate\tType\tYear")
    print("-"*28)
    for plate, ctype, year in rows:
        print(f"{plate}\t{ctype}\t{year}")

def remove_car(plate):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM cars WHERE plate = ?", (plate.strip().upper(),))
    conn.commit()
    if cur.rowcount > 0:
        print(f"Car {plate} removed.")
    else:
        print("❌ No car found with that plate.")
    conn.close()

def main():
    create_table()
    while True:
        try:
            choice = input(MENU).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if choice == "1":
            plate = input("Plate: ").strip().upper()
            car_type = input("Type: ").strip()
            try:
                year = int(input("Year: ").strip())
            except ValueError:
                print("Year must be a number.")
                continue
            add_car(plate, car_type, year)
        elif choice == "2":
            list_cars()
        elif choice == "3":
            plate = input("Plate: ").strip().upper()
            remove_car(plate)
        elif choice == "4":
            print("Bye!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
