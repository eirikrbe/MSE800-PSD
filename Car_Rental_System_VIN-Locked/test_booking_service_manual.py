# test_booking_service_manual.py

from database.database_manager import DatabaseManager
from database.user_queries import add_user
from database.car_queries import add_car, get_car_by_id
from database.booking_queries import get_booking_by_id
from services.fleet_manager import FleetManager
from services.rental_fee_calculator import RentalFeeCalculator
from services.booking_service import BookingService


def print_state(db, booking_id, car_id, label):
    booking = get_booking_by_id(db, booking_id)
    car = get_car_by_id(db, car_id)

    print(f"\n--- {label} ---")
    print("Booking status:", booking["status"])
    print("Car status:", car["status"])
    print("Total fee:", booking["total_fee"])


def test_booking_service_manual():
    print("\n--- Running simple BookingService test ---")

    db = DatabaseManager()

    test_number = 101

    customer_id = add_user(
        db,
        full_name=f"Booking Customer {test_number}",
        email=f"booking_customer{test_number}@example.com",
        phone="555-0000",
        password_hash="fake_hash",
        role="customer"
    )

    car_id = add_car(
        db,
        vin=f"BOOKINGSERVICEVIN{test_number}",
        make="Toyota",
        model="Corolla",
        year=2021,
        mileage=20000,
        daily_rate=50.00,
        min_rent_period=1,
        max_rent_period=30
    )

    fleet_manager = FleetManager.get_instance(db)
    rental_fee_calculator = RentalFeeCalculator()

    booking_service = BookingService(
        db_manager=db,
        fleet_manager=fleet_manager,
        rental_fee_calculator=rental_fee_calculator
    )

    booking_id = booking_service.request_booking(
        customer_id=customer_id,
        car_id=car_id,
        start_date="2026-07-01",
        end_date="2026-07-05"
    )

    print_state(db, booking_id, car_id, "After request_booking")
    # Expected: booking pending, car locked

    booking_service.process_booking_approval(booking_id)
    print_state(db, booking_id, car_id, "After approval")
    # Expected: booking approved, car locked

    booking_service.process_booking_activation(booking_id)
    print_state(db, booking_id, car_id, "After activation")
    # Expected: booking active, car rented

    booking_service.process_booking_completion(booking_id)
    print_state(db, booking_id, car_id, "After completion")
    # Expected: booking completed, car available

    db.disconnect()


if __name__ == "__main__":
    test_booking_service_manual()