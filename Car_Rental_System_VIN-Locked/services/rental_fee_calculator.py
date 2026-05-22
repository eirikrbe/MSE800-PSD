


class RentalFeeCalculator:
    """Encapsulates fee policy (daily rate × days plus fixed booking fee)."""
    BOOKING_FEE = 10.0  

    @staticmethod
    def calculate_fee(daily_rate, booking):
        """Calculate total booking fee: daily_rate * duration + fixed booking fee.

        - Delegates duration calculation to `Booking.calculate_duration()` which
            enforces date validation and returns days as an integer.
        - Adds a constant `BOOKING_FEE` to the variable daily charge.
        """

        duration = booking.calculate_duration()
        return daily_rate * duration + RentalFeeCalculator.BOOKING_FEE
        