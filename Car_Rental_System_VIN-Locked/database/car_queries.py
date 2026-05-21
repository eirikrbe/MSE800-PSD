
# Car_queries.py

ALLOWED_CAR_STATUSES = ["available", "locked", "rented"]

def car_exists(db_manager):
    query = "SELECT 1 FROM cars LIMIT 1"
    return db_manager.fetch_one(query) is not None

def validate_car_status(status):
    if status not in ALLOWED_CAR_STATUSES:
        raise ValueError(f"Invalid car status: {status}. Allowed statuses are: {ALLOWED_CAR_STATUSES}")

def add_car(db_manager, vin, make, model, year, mileage, daily_rate, min_rent_period, max_rent_period):
    query = """
        INSERT INTO cars (vin, make, model, year, mileage, daily_rate, min_rent_period, max_rent_period)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor = db_manager.execute_query(query, (vin, make, model, year, mileage, daily_rate, min_rent_period, max_rent_period))
    return cursor.lastrowid

def get_car_by_vin(db_manager, vin):
    query = "SELECT * FROM cars WHERE vin = ?"
    return db_manager.fetch_one(query, (vin,))

def get_car_by_id(db_manager, car_id):
    query = "SELECT * FROM cars WHERE car_id = ?"
    return db_manager.fetch_one(query, (car_id,))

def get_all_cars(db_manager):
    query = "SELECT * FROM cars"
    return db_manager.fetch_all(query)

def get_cars_by_status(db_manager, status):
    validate_car_status(status)
    query = "SELECT * FROM cars WHERE status = ?"
    return db_manager.fetch_all(query, (status,))

def update_car_status(db_manager, car_id, new_status):
    validate_car_status(new_status)
    query = "UPDATE cars SET status = ? WHERE car_id = ?"
    cursor = db_manager.execute_query(query, (new_status, car_id))
    if cursor.rowcount == 0:
        raise ValueError(f"Car with ID {car_id} does not exist.")
    return True

def update_car_booking_statistics(db_manager, car_id, total_booking_attempts, total_conflicts):
    query = """
        UPDATE cars
        SET total_booking_attempts = ?,
            total_conflicts = ?
        WHERE car_id = ?
    """
    db_manager.execute_query(query, (total_booking_attempts, total_conflicts, car_id))

def update_car(db_manager, car_id, make=None, model=None, year=None, mileage=None, daily_rate=None, min_rent_period=None, max_rent_period=None):
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
        current_car = get_car_by_id(db_manager, car_id)
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
    cursor = db_manager.execute_query(query, tuple(params))
    if cursor.rowcount == 0:
        raise ValueError(f"Car with ID {car_id} does not exist.")
    return True



def delete_car(db_manager, car_id):
    query = "DELETE FROM cars WHERE car_id = ?"
    cursor = db_manager.execute_query(query, (car_id,))
    if cursor.rowcount == 0:
        raise ValueError(f"Car with ID {car_id} does not exist.")
    return True

'''
confidence score
'''

def increment_booking_attempts(db_manager, car_id):
    query = "UPDATE cars SET total_booking_attempts = total_booking_attempts + 1 WHERE car_id = ?"
    db_manager.execute_query(query, (car_id,))

def increment_total_conflicts(db_manager, car_id):
    query = "UPDATE cars SET total_conflicts = total_conflicts + 1 WHERE car_id = ?"
    db_manager.execute_query(query, (car_id,))

