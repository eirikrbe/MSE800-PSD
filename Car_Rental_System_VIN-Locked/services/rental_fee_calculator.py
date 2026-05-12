


class RentalFeeCalculator:
    BOOKING_FEE = 10.0  

    @staticmethod
    def calculate_fee(daily_rate, booking):

        duration = booking.calculate_duration()
        return daily_rate * duration + RentalFeeCalculator.BOOKING_FEE
        