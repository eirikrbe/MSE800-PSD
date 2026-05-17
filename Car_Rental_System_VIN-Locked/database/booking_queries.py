
# booking_queries.py

ALLOWED_STATUSES = [
    "pending",
    "approved",
    "active",
    "rejected",
    "cancelled",
    "completed"
]

def booking_exists(db_manager):
    query = "SELECT 1 FROM bookings LIMIT 1"
    return db_manager.fetch_one(query) is not None

def validate_booking_status(status):
    if status not in ALLOWED_STATUSES:
        raise ValueError(f"Invalid booking status: {status}. Allowed statuses are: {ALLOWED_STATUSES}")


def add_booking(db_manager, customer_id, car_id, start_date, end_date, total_fee, status="pending"):
    validate_booking_status(status)
    query = """
        INSERT INTO bookings (customer_id, car_id, start_date, end_date, total_fee, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor = db_manager.execute_query(
        query,
        (customer_id, car_id, start_date, end_date, total_fee, status)
    )
    return cursor.lastrowid


def get_booking_by_id(db_manager, booking_id):
    query = "SELECT * FROM bookings WHERE booking_id = ?"
    return db_manager.fetch_one(query, (booking_id,))


def get_bookings_by_customer(db_manager, customer_id):
    query = "SELECT * FROM bookings WHERE customer_id = ?"
    return db_manager.fetch_all(query, (customer_id,))


def get_bookings_by_car(db_manager, car_id):
    query = "SELECT * FROM bookings WHERE car_id = ?"
    return db_manager.fetch_all(query, (car_id,))


def get_bookings_by_status(db_manager, status):
    validate_booking_status(status)

    query = "SELECT * FROM bookings WHERE status = ?"
    return db_manager.fetch_all(query, (status,))


def get_all_bookings(db_manager):
    query = "SELECT * FROM bookings"
    return db_manager.fetch_all(query)


def update_booking_status(db_manager, booking_id, new_status):
    validate_booking_status(new_status)

    query = "UPDATE bookings SET status = ? WHERE booking_id = ?"
    cursor = db_manager.execute_query(query, (new_status, booking_id))

    if cursor.rowcount == 0:
        raise ValueError(f"Booking with ID {booking_id} does not exist.")
    
    return True
