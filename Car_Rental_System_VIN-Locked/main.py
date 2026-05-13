
# main.py


from database.database_manager import DatabaseManager
from services.auth_service import AuthService
from services.fleet_manager import FleetManager
from services.booking_service import BookingService
from services.rental_fee_calculator import RentalFeeCalculator
from cli.main_menu import main_menu


def main():
    db = DatabaseManager()
    fleet_manager = FleetManager.get_instance(db)
    rental_fee_calculator = RentalFeeCalculator()
    auth_service = AuthService(db)
    booking_service = BookingService(db, fleet_manager, rental_fee_calculator)
    
    try:
        main_menu(auth_service, booking_service, fleet_manager)
    finally:
        db.disconnect()

if __name__ == "__main__":
    main()