
# booking_service.py


from models.car import Car
from models.booking import Booking
from database.booking_queries import (
    add_booking,
    get_bookings_by_customer,
    update_booking_status,
    get_booking_by_id,
    get_bookings_by_status,
    booking_exists as db_booking_exists
)


class BookingService:
    """Orchestrates booking lifecycle, validations, vehicle coordination and persistence."""
    def __init__(self, db_manager, fleet_manager, rental_fee_calculator):
        self.db_manager = db_manager
        self.fleet_manager = fleet_manager
        self.rental_fee_calculator = rental_fee_calculator

    def booking_exists(self):
        return db_booking_exists(self.db_manager)

    def request_booking(self, customer_id, car_id, start_date, end_date):
        """Create a booking request and return its DB id.

        Business rules and side effects:
        - Validates car existence and availability; raises `ValueError` if invalid.
        - Expects `start_date` and `end_date` as 'YYYY-MM-DD' strings.
        - Ensures requested period satisfies car's min/max rent period via
          `Car.is_rent_period_valid`.
        - Records a booking attempt and checks for date conflicts; conflicts
          increment the car's conflict counter and block the booking.
        - Locks the vehicle (`fleet_manager.lock_vehicle`) before persisting
          the booking to reduce race conditions; note this is not wrapped in
          an atomic DB transaction in current implementation.
        - Calculates total fee via `rental_fee_calculator.calculate_fee`.
        - Inserts the booking with status 'pending' and returns the new id.
        """

        car_row = self.fleet_manager.get_car_by_id(car_id)

        if not car_row:
            raise ValueError(f"Car with ID {car_id} does not exist.")

        car = Car.from_row(car_row)

        if not self.fleet_manager.check_car_availability(car_id):
            raise ValueError(f"Car with ID {car_id} is not available for booking.")

        if not car.is_rent_period_valid(start_date, end_date):
            raise ValueError(
                "Requested rental period does not meet the car's minimum and maximum rent period requirements."
            )

        self.fleet_manager.record_booking_attempt(car_id)

        if self.fleet_manager.check_date_conflict(car_id, start_date, end_date):
            raise ValueError(
                f"Car with ID {car_id} has a conflicting booking during the requested dates."
            )

        booking = Booking(customer_id, car_id, start_date, end_date, "pending")

        total_booking_fee = self.rental_fee_calculator.calculate_fee(car.daily_rate, booking)
        booking.total_fee = total_booking_fee
        '''
        Future improvement: wrap vehicle locking and booking creation in a database transaction.
        Locking first reduces the risk of double-booking, but if booking creation fails,
        the car may remain locked without a booking and require recovery handling.
        '''
        
        self.fleet_manager.lock_vehicle(car_id)

        booking_id = add_booking(
            self.db_manager,
            customer_id,
            car_id,
            start_date,
            end_date,
            total_booking_fee,
            "pending"
        )

        return booking_id
    
    def process_booking_approval(self, booking_id):
        """Approve a pending booking and return the updated booking row.

        Preconditions and effects:
        - Booking must exist and be in 'pending' state; otherwise raises ValueError.
        - Transitions booking.status -> 'approved' in the DB via `update_booking_status`.
        - Does not automatically change vehicle lock state; callers (admin UI)
          should manage vehicle lifecycle (activation will mark rented).
        """
        booking = get_booking_by_id(self.db_manager, booking_id)

        if not booking:
            raise ValueError(f"Booking with ID {booking_id} does not exist.")

        if booking["status"] != "pending":
            raise ValueError(f"Booking with ID {booking_id} is not pending and cannot be approved.")

        update_booking_status(self.db_manager, booking_id, "approved")

        updated_booking = get_booking_by_id(self.db_manager, booking_id)
        
        return updated_booking
    
    def process_booking_rejection(self, booking_id):
        """Reject a pending booking, release any locked vehicle, and return updated row.

        - Ensures booking exists and is 'pending'.
        - Sets booking.status -> 'rejected' and calls `fleet_manager.release_vehicle`
          to return the car to 'available' state.
        """
        booking = get_booking_by_id(self.db_manager, booking_id)

        if not booking:
            raise ValueError(f"Booking with ID {booking_id} does not exist.")

        if booking["status"] != "pending":
            raise ValueError(f"Booking with ID {booking_id} is not pending and cannot be rejected.")
        
        update_booking_status(self.db_manager, booking_id, "rejected")

        self.fleet_manager.release_vehicle(booking["car_id"])

        updated_booking = get_booking_by_id(self.db_manager, booking_id)
        
        return updated_booking 
    
    def process_booking_activation(self, booking_id):
        """Activate an approved booking and mark the vehicle as rented.

        - Booking must exist and be in 'approved' state.
        - Transitions booking.status -> 'active' and calls
          `fleet_manager.mark_vehicle_rented` which enforces status transition
          from 'locked' -> 'rented'.
        """
        booking = get_booking_by_id(self.db_manager, booking_id)

        if not booking:
            raise ValueError(f"Booking with ID {booking_id} does not exist.")

        if booking["status"] != "approved":
            raise ValueError(f"Booking with ID {booking_id} is not approved and cannot be activated.")
        
        update_booking_status(self.db_manager, booking_id, "active")

        self.fleet_manager.mark_vehicle_rented(booking["car_id"])

        updated_booking = get_booking_by_id(self.db_manager, booking_id)
        
        return updated_booking
    
    def process_booking_completion(self, booking_id):
        """Complete an active booking and release the vehicle back to available.

        - Validates the booking exists and is 'active'.
        - Sets booking.status -> 'completed' and calls
          `fleet_manager.release_vehicle` to set car to 'available'.
        """
        booking = get_booking_by_id(self.db_manager, booking_id)

        if not booking:
            raise ValueError(f"Booking with ID {booking_id} does not exist.")

        if booking["status"] != "active":
            raise ValueError(f"Booking with ID {booking_id} is not active and cannot be completed.")
        
        update_booking_status(self.db_manager, booking_id, "completed")

        self.fleet_manager.release_vehicle(booking["car_id"])

        updated_booking = get_booking_by_id(self.db_manager, booking_id)
        
        return updated_booking

    def process_booking_cancellation(self, booking_id):
        """Cancel a pending or approved booking and free the vehicle.

        - Allowed source states: 'pending' or 'approved'; other states raise ValueError.
        - Transitions booking.status -> 'cancelled' and calls
          `fleet_manager.release_vehicle` to make the car available again.
        """
        booking = get_booking_by_id(self.db_manager, booking_id)

        if not booking:
            raise ValueError(f"Booking with ID {booking_id} does not exist.")

        if booking["status"] not in ["pending", "approved"]:
            raise ValueError(f"Booking with ID {booking_id} cannot be cancelled at its current status.")
        
        update_booking_status(self.db_manager, booking_id, "cancelled")

        self.fleet_manager.release_vehicle(booking["car_id"])

        updated_booking = get_booking_by_id(self.db_manager, booking_id)
        
        return updated_booking
    
    def get_customer_bookings(self, customer_id):
        return get_bookings_by_customer(self.db_manager, customer_id)

    def get_bookings_by_status(self, status):
        return get_bookings_by_status(self.db_manager, status)

        
