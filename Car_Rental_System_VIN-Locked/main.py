
# main.py


from database.database_manager import DatabaseManager
from services.auth_service import AuthService
from setup.bootstrap import run_app_setup
from services.fleet_manager import FleetManager
from services.booking_service import BookingService
from services.rental_fee_calculator import RentalFeeCalculator
from cli.main_menu import main_menu
from cli.display_helpers import (
    pause,
    display_title,
    display_success,
    )


def main():
    
    db = DatabaseManager()
    fleet_manager = FleetManager.get_instance(db)
    rental_fee_calculator = RentalFeeCalculator()
    auth_service = AuthService(db)
    booking_service = BookingService(db, fleet_manager, rental_fee_calculator)
    setup_result = run_app_setup(auth_service, fleet_manager, booking_service)

    if setup_result["admin"]:
        display_title("Default admin account created.")
        print("Email: admin")
        print("Password: admin")

    if setup_result["customer"]:
        display_title("Demo customer account created.")
        print("Email: customer")
        print("Password: customer")

    if setup_result["cars"]:
        display_title("Default cars created.")

    if setup_result["booking"]:
        display_title("Default booking created.")

    if any(setup_result.values()):
        display_success("Setup completed.")
        pause()

    try:

        main_menu(auth_service, booking_service, fleet_manager)

    finally:
        db.disconnect()

if __name__ == "__main__":

    main()