
# fleet_manager.py

from datetime import datetime

from database.booking_queries import get_bookings_by_car
from database.car_queries import (
    get_all_cars as db_get_all_cars,
    get_car_by_id,
    increment_booking_attempts,
    increment_total_conflicts,
    update_car_status,
    get_cars_by_status,
    add_car as db_add_car,
    get_car_by_vin,
    update_car as db_update_car,
    delete_car as db_delete_car,
    update_car_booking_statistics
)


class FleetManager:
    """Manages vehicle state, availability, metrics and confidence scoring for the fleet."""
    _instance = None

    @classmethod
    def get_instance(cls, db_manager):
        """Return a singleton `FleetManager` for the given `db_manager`.

        Pattern: implements a simple module-level singleton to ensure shared
        in-memory state (e.g. booking attempts and conflict recording) is
        concentrated in a single manager instance.
        """
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
        """Validate car attribute ranges and relational constraints.

        Rules enforced:
        - `year` must be within sensible bounds (1900-2100).
        - `mileage` and `daily_rate` must be non-negative and positive respectively.
        - `min_rent_period` and `max_rent_period` must be positive and
          `min_rent_period` cannot exceed `max_rent_period` when both provided.
        Raises `ValueError` on violation.
        """
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
        """Check for overlapping bookings for a car.

        - Parses `start_date`/`end_date` as 'YYYY-MM-DD'.
        - Raises `ValueError` if the requested end is not after start.
        - Ignores bookings in terminal states: 'cancelled', 'completed', 'rejected'.
        - If an overlap is detected, increments conflict counter via
          `record_conflict` and returns True; otherwise returns False.
        """
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
                self.record_conflict(car_id)
                return True
        return False

    def lock_vehicle(self, car_id):
        """Transition vehicle to 'locked' to reserve it for booking creation.

        - Enforces that only `available` cars can be locked; raises `ValueError`
            otherwise.
        - Persists the status change via `update_car_status`.
        - This method is used to reduce double-booking windows prior to
            inserting a booking record.
        """
        car = self.get_car_by_id(car_id)
        if car["status"] != "available":
                raise ValueError(f"Car with ID {car_id} is not available for locking.")
        update_car_status(self.db_manager, car_id, "locked")
        return True

    def release_vehicle(self, car_id):
        """Release a vehicle back to 'available' state from 'locked' or 'rented'.

        - Validates current status is one that can be released.
        - Persists the transition via `update_car_status`.
        """
        car = self.get_car_by_id(car_id)
        if car["status"] not in ["locked", "rented"]:
            raise ValueError(f"Car with ID {car_id} is not currently locked or rented.")
        update_car_status(self.db_manager, car_id, "available")
        return True

    def mark_vehicle_rented(self, car_id):
        """Mark a locked vehicle as rented when a booking is activated.

        - Enforces the state transition from 'locked' -> 'rented'.
        - Raises ValueError if caller attempts to mark a non-locked vehicle.
        """
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
        """Validate attributes, enforce VIN uniqueness, and persist a new car record."""
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
        """Validate requested field updates (e.g., mileage non-decreasing) and persist changes."""
        
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
    
    def update_car_booking_statistics(self, car_id, total_booking_attempts, total_conflicts):
        if total_booking_attempts < 0:
            raise ValueError("Booking attempts cannot be negative.")

        if total_conflicts < 0:
            raise ValueError("Total conflicts cannot be negative.")

        if total_conflicts > total_booking_attempts:
            raise ValueError("Total conflicts cannot exceed booking attempts.")

        update_car_booking_statistics(
            self.db_manager,
            car_id,
            total_booking_attempts,
            total_conflicts
        )
    
    '''
    confidence score
    '''

    def calculate_booking_reliability_score(self, car_id):
        """Calculate a reliability sub-score from the vehicle's booking history."""
        bookings = get_bookings_by_car(self.db_manager, car_id)
        
        completed = 0
        total_relevant = 0
        
        for booking in bookings:
            if booking["status"] == "rejected":
                continue
            total_relevant += 1
            if booking["status"] == "completed":
                completed += 1
        
        if total_relevant == 0:
            return 75  # default for new cars
        
        return (completed / total_relevant) * 100
    
    def calculate_mileage_score(self, car):
        """Return a 0–100 score reflecting mileage-related condition; higher is better."""
        mileage = car["mileage"]
        return max(0, (1 - mileage / 200000) * 100)
    
    def calculate_vehicle_age_score(self, car):
        """Return a 0–100 score reflecting vehicle age; newer cars score higher."""
        current_year = datetime.now().year
        age = current_year - car["year"]
        return max(0, (1 - age / 20) * 100)
    
    def calculate_conflict_score(self, car):
        """Return a 0–100 score derived from conflict rate with sensible fallbacks."""
        attempts = car["total_booking_attempts"]
        conflicts = car["total_conflicts"]
        
        if attempts == 0:
            return 75  # default for new cars
        
        return min(100, max(0, (1 - conflicts / attempts) * 100))
    
    def calculate_confidence_score(self, car_id):
        """Compute an overall confidence score used for ranking vehicles.

        Composition and rationale:
        - Aggregates four sub-scores (reliability, mileage, age, conflict)
            with tunable weights (40/25/20/15 respectively).
        - Sub-scores use sensible defaults for new vehicles (e.g., 75)
            so that newcomers are not penalized excessively.
        - Returns a rounded float (1 decimal) intended for display only; it
            does not alter persistent state.
        """
        car = self.get_car_by_id(car_id)

        reliability = self.calculate_booking_reliability_score(car_id)
        mileage = self.calculate_mileage_score(car)
        age = self.calculate_vehicle_age_score(car)
        conflict = self.calculate_conflict_score(car)

        score = (
                reliability * 0.40 +
                mileage     * 0.25 +
                age         * 0.20 +
                conflict    * 0.15
        )

        return round(score, 1)
    
    def record_booking_attempt(self, car_id):
        """Atomically increment booking-attempt counter for analytics and scoring."""
        increment_booking_attempts(self.db_manager, car_id)

    def record_conflict(self, car_id):
        """Atomically increment conflict counter when overlapping bookings occur."""
        increment_total_conflicts(self.db_manager, car_id)
