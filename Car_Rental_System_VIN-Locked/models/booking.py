

from datetime import datetime


class Booking:
    def __init__(self, customer_id, car_id, start_date, end_date, status, booking_id=None, total_fee=0):
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.car_id = car_id
        self.start_date = start_date
        self.end_date = end_date
        self.total_fee = total_fee
        self.status = status    

    def get_booking_details(self):
        return {
            "booking_id": self.booking_id,
            "customer_id": self.customer_id,
            "car_id": self.car_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "total_fee": self.total_fee,
            "status": self.status
        }

    def calculate_duration(self):
        """Return the rental duration in days and validate date order.

        - Parses `start_date` and `end_date` as 'YYYY-MM-DD'.
        - Returns integer number of days (end - start).
        - Raises `ValueError` if duration is not positive.
        """
        start = datetime.strptime(self.start_date, "%Y-%m-%d")
        end = datetime.strptime(self.end_date, "%Y-%m-%d")
        duration = (end - start).days
        if duration <= 0:
            raise ValueError("End date must be after start date")
        return duration
    