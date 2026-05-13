
# car.py

from datetime import datetime


class Car:
    def __init__(self, vin, make, model, year, mileage, daily_rate, status="available", min_rent_period=1, max_rent_period=30, total_booking_attempts=0, total_conflicts=0, car_id=None):
        self.car_id = car_id
        self.vin = vin
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.daily_rate = daily_rate
        self.status = status
        self.min_rent_period = min_rent_period
        self.max_rent_period = max_rent_period
        self.total_booking_attempts = total_booking_attempts
        self.total_conflicts = total_conflicts


    def get_car_details(self):
        return {
            "car_id": self.car_id,
            "vin": self.vin,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "mileage": self.mileage,
            "daily_rate": self.daily_rate,
            "status": self.status,
            "min_rent_period": self.min_rent_period,
            "max_rent_period": self.max_rent_period,
            "total_booking_attempts": self.total_booking_attempts,
            "total_conflicts": self.total_conflicts
        }
    
    @classmethod
    def from_row(cls, row):
        return cls(
            car_id=row["car_id"],
            vin=row["vin"],
            make=row["make"],
            model=row["model"],
            year=row["year"],
            mileage=row["mileage"],
            daily_rate=row["daily_rate"],
            status=row["status"],
            min_rent_period=row["min_rent_period"],
            max_rent_period=row["max_rent_period"],
            total_booking_attempts=row["total_booking_attempts"],
            total_conflicts=row["total_conflicts"]
        )
    
    def is_rent_period_valid(self, start_date, end_date):
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()

        duration = (end - start).days

        return self.min_rent_period <= duration <= self.max_rent_period