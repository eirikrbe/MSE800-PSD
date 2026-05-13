
# booking_service.py


from models.car import Car
from models.booking import Booking
from database.booking_queries import add_booking, update_booking_status, get_booking_by_id


class BookingService:
    def __init__(self, db_manager, fleet_manager, rental_fee_calculator):
        self.db_manager = db_manager
        self.fleet_manager = fleet_manager
        self.rental_fee_calculator = rental_fee_calculator

    def request_booking(self, customer_id, car_id, start_date, end_date):

        car = Car.from_row(self.fleet_manager.get_car_by_id(car_id))

        if not self.fleet_manager.check_car_availability(car_id):
            raise ValueError(f"Car with ID {car_id} is not available for booking.")
        if self.fleet_manager.check_date_conflict(car_id, start_date, end_date):
            raise ValueError(f"Car with ID {car_id} has a conflicting booking during the requested dates.")
        
        if not car.is_rent_period_valid(start_date, end_date):
            raise ValueError("Requested rental period does not meet the car's minimum and maximum rent period requirements.")
        

        booking = Booking(customer_id, car_id, start_date, end_date, "pending")

        total_booking_fee = self.rental_fee_calculator.calculate_fee(car.daily_rate, booking)
        booking.total_fee = total_booking_fee

        self.fleet_manager.lock_vehicle(car_id) #Future improvement: wrap booking creation and vehicle locking in a database transaction to ensure atomicity.

        booking_id = add_booking(self.db_manager, customer_id, car_id, start_date, end_date, total_booking_fee, "pending")
        return booking_id
    
    def process_booking_approval(self, booking_id):
        booking = get_booking_by_id(self.db_manager, booking_id)

        if not booking:
            raise ValueError(f"Booking with ID {booking_id} does not exist.")

        if booking["status"] != "pending":
            raise ValueError(f"Booking with ID {booking_id} is not pending and cannot be approved.")

        update_booking_status(self.db_manager, booking_id, "approved")

        updated_booking = get_booking_by_id(self.db_manager, booking_id)
        
        return updated_booking
    
    def process_booking_rejection(self, booking_id):
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
        booking = get_booking_by_id(self.db_manager, booking_id)

        if not booking:
            raise ValueError(f"Booking with ID {booking_id} does not exist.")

        if booking["status"] not in ["pending", "approved"]:
            raise ValueError(f"Booking with ID {booking_id} cannot be cancelled at its current status.")
        
        update_booking_status(self.db_manager, booking_id, "cancelled")

        self.fleet_manager.release_vehicle(booking["car_id"])

        updated_booking = get_booking_by_id(self.db_manager, booking_id)
        
        return updated_booking

        
