
# fleet_manager.py

from datetime import datetime

from database.booking_queries import get_bookings_by_car
from database.car_queries import (
    get_all_cars as db_get_all_cars,
    get_car_by_id,
    update_car_status,
    get_cars_by_status,
    add_car as db_add_car,
    get_car_by_vin,
    update_car as db_update_car,
    delete_car as db_delete_car
)


class FleetManager:
    _instance = None

    @classmethod
    def get_instance(cls, db_manager):
        if cls._instance is None:
            cls._instance = cls(db_manager)
        return cls._instance

    def __init__(self, db_manager):
        self.db_manager = db_manager
 
    def _validate_car_data(
        self,
        year=None,
        mileage=None,
        daily_rate=None,
        min_rent_period=None,
        max_rent_period=None
        ):
        if year is not None and (year < 1900 or year > 2100):
            raise ValueError("Invalid year.")

        if mileage is not None and mileage < 0:
            raise ValueError("Mileage cannot be negative.")

        if daily_rate is not None and daily_rate <= 0:
            raise ValueError("Daily rate must be greater than zero.")

        if min_rent_period is not None and min_rent_period <= 0:
            raise ValueError("Minimum rent period must be greater than zero.")

        if max_rent_period is not None and max_rent_period <= 0:
            raise ValueError("Maximum rent period must be greater than zero.")

        if (
            min_rent_period is not None
            and max_rent_period is not None
            and min_rent_period > max_rent_period
        ):
            raise ValueError("Minimum rent period cannot be greater than maximum rent period.")

        return True

    def get_car_by_id(self, car_id):
        car = get_car_by_id(self.db_manager, car_id)
        if not car:
            raise ValueError(f"Car with ID {car_id} does not exist.")
        return car
    
    def get_car_by_vin(self, vin):
        car = get_car_by_vin(self.db_manager, vin)
        if not car:
            raise ValueError(f"Car with VIN {vin} does not exist.")
        return car
    
    def car_exists_by_vin(self, vin):
        car = get_car_by_vin(self.db_manager, vin)
        return car is not None

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
    
    def get_all_cars(self):
        return db_get_all_cars(self.db_manager)
    
    def delete_car(self, car_id):
        self.get_car_by_id(car_id)
        return db_delete_car(self.db_manager, car_id)
       
    def add_car(self, vin, make, model, year, mileage, daily_rate, min_rent_period, max_rent_period):
        existing_car = get_car_by_vin(self.db_manager, vin)
        if existing_car:
            raise ValueError("A car with this VIN already exists.")
        
        self._validate_car_data(
            year=year,
            mileage=mileage,
            daily_rate=daily_rate,
            min_rent_period=min_rent_period,
            max_rent_period=max_rent_period
         )
  
        return db_add_car(self.db_manager, vin, make, model, year, mileage, daily_rate, min_rent_period, max_rent_period)

    def update_car(self, car_id, make=None, model=None, year=None, mileage=None, daily_rate=None, min_rent_period=None, max_rent_period=None):
        
        current_car = self.get_car_by_id(car_id)

        final_min_rent_period = (
        min_rent_period
            if min_rent_period is not None
            else current_car["min_rent_period"]
        )

        final_max_rent_period = (
        max_rent_period
            if max_rent_period is not None
            else current_car["max_rent_period"]
        )

        self._validate_car_data(
            year=year,
            mileage=mileage,
            daily_rate=daily_rate,
            min_rent_period=final_min_rent_period,
            max_rent_period=final_max_rent_period
        )

        return db_update_car(
            self.db_manager,
            car_id,
            make,
            model,
            year,
            mileage,
            daily_rate,
            min_rent_period,
            max_rent_period
        )
    

