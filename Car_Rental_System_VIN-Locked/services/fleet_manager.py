
# fleet_manager.py

from datetime import datetime
from database.car_queries import get_car_by_id, update_car_status, get_cars_by_status
from database.booking_queries import get_bookings_by_car

class FleetManager:
    _instance = None

    @classmethod
    def get_instance(cls, db_manager):
        if cls._instance is None:
            cls._instance = cls(db_manager)
        return cls._instance

    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_car_by_id(self, car_id):
        car = get_car_by_id(self.db_manager, car_id)
        if not car:
            raise ValueError(f"Car with ID {car_id} does not exist.")
        return car

    def check_car_availability(self, car_id):
        car = self.get_car_by_id(car_id)
        return car["status"] == "available"
    
    def check_date_conflict(self, car_id, start_date, end_date):
        new_start = datetime.strptime(start_date, "%Y-%m-%d")
        new_end = datetime.strptime(end_date, "%Y-%m-%d")
        if new_start >= new_end:
            raise ValueError("End date must be after start date.")
        bookings = get_bookings_by_car(self.db_manager, car_id)
        for booking in bookings:
            ignore_booking = booking["status"] in ["cancelled", "completed", "rejected"]
            if ignore_booking:
                continue
            existing_start = datetime.strptime(booking["start_date"], "%Y-%m-%d")
            existing_end = datetime.strptime(booking["end_date"], "%Y-%m-%d")
            if (new_start < existing_end) and (new_end > existing_start):
                return True
        return False

    def lock_vehicle(self, car_id):
        car = self.get_car_by_id(car_id)
        if car["status"] != "available":
            raise ValueError(f"Car with ID {car_id} is not available for locking.")
        update_car_status(self.db_manager, car_id, "locked")
        return True

    def release_vehicle(self, car_id):
        car = self.get_car_by_id(car_id)
        if car["status"] not in ["locked", "rented"]:
            raise ValueError(f"Car with ID {car_id} is not currently locked or rented.")
        update_car_status(self.db_manager, car_id, "available")
        return True

    def mark_vehicle_rented(self, car_id):
        car = self.get_car_by_id(car_id)
        if car["status"] != "locked":
            raise ValueError(f"Car with ID {car_id} must be locked before marking as rented.")
        update_car_status(self.db_manager, car_id, "rented")
        return True
    
    def get_available_cars(self):
        return get_cars_by_status(self.db_manager, "available")
    
