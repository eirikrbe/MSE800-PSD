

from database.database_manager import DatabaseManager
from database.user_queries import add_user
from database.car_queries import add_car, get_car_by_id, update_car_status
from database.booking_queries import add_booking
from services.fleet_manager import FleetManager


def run_fleet_manager_tests():
    print("\n--- Running FleetManager tests ---")
    db = DatabaseManager()
    print("Connection active:", db.get_connection() is not None)

    test_number = 9
    email = f"fleet_customer{test_number}@example.com"

    customer_id = add_user(
        db,
        full_name=f"Fleet Customer {test_number}",
        email=email,
        phone="555-0000",
        password_hash="fake_hash",
        role="customer"
    )
    
    print(f"Inserted customer with ID: {customer_id}")


    vin = f"FLEETTESTVIN{test_number}"

    car_id = add_car(
        db,
        vin=vin,
        make=f"Toyota {test_number}",
        model="Corolla",
        year=2021,
        mileage=20000,
        daily_rate=50.00,
        min_rent_period=1,
        max_rent_period=30
    )

    print(f"Inserted car with ID: {car_id}")

    fleet_manager = FleetManager.get_instance(db)

    print("\n--- Testing check_car_availability ---")
    print("Car availability (should be True):", fleet_manager.check_car_availability(car_id))

    fleet_manager.lock_vehicle(car_id)
    car = get_car_by_id(db, car_id)
    print("Car status after locking (should be 'locked'):", car["status"])

    print("\n--- Testing release_vehicle ---")
    fleet_manager.release_vehicle(car_id)
    car = get_car_by_id(db, car_id)
    print("Car status after releasing (should be 'available'):", car["status"])

    print("\n--- Testing mark_vehicle_rented ---")
    fleet_manager.lock_vehicle(car_id)
    fleet_manager.mark_vehicle_rented(car_id)
    car = get_car_by_id(db, car_id)
    print("Car status after marking as rented (should be 'rented'):", car["status"])

    update_car_status(db, car_id, "available")

    add_booking(
        db,
        customer_id=customer_id,
        car_id=car_id,
        start_date="2026-05-01",
        end_date="2026-05-04",
        total_fee=150,
        status="approved"
    )

    conflict = fleet_manager.check_date_conflict(
        car_id,
        "2026-05-03",
        "2026-05-06"
    )

    print("Overlap conflict (should be True)", conflict)

    conflict = fleet_manager.check_date_conflict(
        car_id,
        "2026-05-04",
        "2026-05-06"
    )

    print("Back-to-back conflict (should be False):", conflict)

    add_booking(
        db,
        customer_id=customer_id,
        car_id=car_id,
        start_date="2026-06-01",
        end_date="2026-06-05",
        total_fee=200,
        status="cancelled"
    )

    conflict = fleet_manager.check_date_conflict(
        car_id,
        "2026-06-02",
        "2026-06-04"
    )

    print("Cancelled booking conflict (should be False):", conflict)

    try:
        fleet_manager.check_date_conflict(car_id, "2026-05-10", "2026-05-01")
        print("ERROR: Invalid date range was accepted.")
    except ValueError as e:
        print("Invalid date range rejected correctly:", e)

    try:
        fleet_manager.check_car_availability(999999)
        print("ERROR: Fake car ID was accepted.")
    except ValueError as e:
        print("Fake car ID rejected correctly:", e)

    db.disconnect()
    print("Disconnected successfully.")

if __name__ == "__main__":
    run_fleet_manager_tests()