
from database.database_manager import DatabaseManager

from database.car_queries import (
    add_car,
    get_all_cars,
    get_car_by_id,
    get_car_by_vin,
    update_car_status,
    update_car,
    delete_car
)

from database.user_queries import (
    add_user,
    get_user_by_email,
    get_user_by_id
)

from database.booking_queries import (
    add_booking,
    get_booking_by_id,
    get_bookings_by_customer,
    get_bookings_by_car,
    get_bookings_by_status,
    get_all_bookings,
    update_booking_status
)

def test_database_connection():
    print("\n--- Testing database connection ---")

    db = DatabaseManager()

    connection = db.get_connection()
    print("Connection active:", connection is not None)

    # -----------------------------
    # TEST CAR QUERIES
    # -----------------------------
    print("\n--- Testing car queries ---")

    car_id = add_car(
        db,
        vin="test6vin123456789",
        make="TestMake6",
        model="testmode6",
        year=2020,
        mileage=15000,
        daily_rate=49.99,
        min_rent_period=1,
        max_rent_period=30
    )

    print(f"Inserted car with ID: {car_id}")

    car = get_car_by_id(db, car_id)
    print("Retrieved car by ID:", dict(car))

    car_by_vin = get_car_by_vin(db, "test6vin123456789")
    print("Retrieved car by VIN:", dict(car_by_vin))

    update_car_status(db, car_id, "locked")
    car = get_car_by_id(db, car_id)
    print(f"Updated car status: {car['status']}")

    update_car(db, car_id, mileage=16000, daily_rate=59.99)
    car = get_car_by_id(db, car_id)
    print(f"Updated car mileage: {car['mileage']}, daily rate: {car['daily_rate']}")

    try:
        update_car(db, car_id, mileage=14000)
        print("ERROR: Mileage validation failed.")
    except ValueError as e:
        print("Mileage validation works:", e)

    cars = get_all_cars(db)
    print("\nCars table query result:")

    if cars:
        for car in cars:
            print(dict(car))
    else:
        print("No cars found.")


    # -----------------------------
    # TEST USER QUERIES
    # -----------------------------
    print("\n--- Testing user queries ---")

    customer_id = add_user(
        db,
        full_name="Customer6",
        email="customer6@example.com",
        phone="555-5678",
        password_hash="customer6_fake_hash",
        role="customer"
    )

    print(f"Inserted user with ID: {customer_id}")

    user_by_email = get_user_by_email(db, "customer6@example.com")
    print(f"Retrieved user by email: {user_by_email['full_name']}")

    user_by_id = get_user_by_id(db, customer_id)
    print(f"Retrieved user by ID: {user_by_id['full_name']}")

    # -----------------------------
    # TEST BOOKING QUERIES
    # -----------------------------
    print("\n--- Testing booking queries ---")
    
    booking_id = add_booking(
        db,
        customer_id=customer_id,
        car_id=car_id,
        start_date="2024-07-01",
        end_date="2024-07-05",
        total_fee=199.95,
        status="pending"
    )

    print(f"Inserted booking with ID: {booking_id}")

    booking = get_booking_by_id(db, booking_id)
    print("Retrieved booking by ID:", dict(booking))

    bookings_by_customer = get_bookings_by_customer(db, customer_id)    
    print("Retrieved bookings by customer:")

    for booking in bookings_by_customer:
        print(dict(booking))

    bookings_by_car = get_bookings_by_car(db, car_id)
    print("Retrieved bookings by car:")
    for booking in bookings_by_car:
        print(dict(booking))
    
    bookings_by_status = get_bookings_by_status(db, "pending")
    print("Retrieved bookings by status:")
    for booking in bookings_by_status:
        print(dict(booking))

    update_booking_status(db, booking_id, "approved")
    booking = get_booking_by_id(db, booking_id)
    print(f"Updated booking status: {booking['status']}")


    bookings = get_all_bookings(db)
    print("\nBookings table query result:")
    if bookings:
        for booking in bookings:
            print(dict(booking))
    else:
        print("No bookings found.")

    # -----------------------------
    # TEST DISCONNECT
    # -----------------------------
    print("\n--- Testing disconnect ---")

    db.disconnect()
    print("Disconnected successfully.")

    try:
        db.get_connection()
        print("ERROR: get_connection() should have failed after disconnect.")
    except ConnectionError:
        print("ConnectionError works correctly after disconnect.")


if __name__ == "__main__":
    test_database_connection()