class Flight:
    '''
    Parent class that stores the general flight information.
    '''
    def __init__(self, flightNumber, departureAirport, arrivalAirport, **kwargs):
        super().__init__(**kwargs)
        self.flightNumber = flightNumber
        self.departureAirport = departureAirport
        self.arrivalAirport = arrivalAirport
        self.status = "Created"

    def get_flight_details(self):
        return (
            f"Flight Number = {self.flightNumber}, "
            f"Departure Airport = {self.departureAirport}, "
            f"Arrival Airport = {self.arrivalAirport}, "
            f"Status = {self.status}"
        )

    def schedule_flight(self):
        self.status = "Scheduled"
        return f"Flight {self.flightNumber} has been scheduled."

    def cancel_flight(self):
        self.status = "Cancelled"
        return f"Flight {self.flightNumber} has been cancelled."


class DomesticFlight(Flight):
    '''
    Child class for flights within the same country.
    '''
    def __init__(self, regionCode, **kwargs):
        super().__init__(**kwargs)
        self.regionCode = regionCode

    def validate_domestic_route(self):
        return self.departureAirport != self.arrivalAirport

    def calculate_domestic_fee(self):
        return 25.00

    def get_route_info(self):
        return (
            f"Domestic route: {self.departureAirport} to {self.arrivalAirport}, "
            f"Region = {self.regionCode}"
        )


class InternationalFlight(Flight):
    '''
    Child class for flights between different countries.
    '''
    def __init__(self, countryCode, visaRequirement, **kwargs):
        super().__init__(**kwargs)
        self.countryCode = countryCode
        self.visaRequirement = visaRequirement

    def check_passport(self):
        return True

    def calculate_customs_fee(self):
        return 75.00

    def get_terminal_info(self):
        return (
            f"International terminal for country code {self.countryCode}. "
            f"Visa Requirement = {self.visaRequirement}"
        )


class HybridFlight(DomesticFlight, InternationalFlight):
    '''
    Child class that uses hybrid inheritance by combining domestic and international flight features.
    '''
    def __init__(self, isConnecting, transitAirport, transitVisa, **kwargs):
        super().__init__(**kwargs)
        self.isConnecting = isConnecting
        self.transitAirport = transitAirport
        self.transitVisa = transitVisa

    def process_transit(self):
        if self.isConnecting:
            return f"Transit processed at {self.transitAirport}. Transit Visa = {self.transitVisa}"
        return "No transit process needed."

    def update_manifest(self):
        return f"Passenger manifest updated for flight {self.flightNumber}."

    def get_route_info(self):
        # This method explains the hybrid route between domestic to international, overrides the domestic version, because hybrid version needs its own route explanation
        return (
            f"Connecting route: {self.departureAirport} to {self.transitAirport} "
            f"to {self.arrivalAirport}, Domestic Region = {self.regionCode}, "
            f"International Country Code = {self.countryCode}"
        )

    def calculate_total_cost(self):
        # This method uses behaviour from both parent classes.
        return self.calculate_domestic_fee() + self.calculate_customs_fee()


if __name__ == "__main__":

    domestic1 = DomesticFlight(
        flightNumber="NZ123",
        departureAirport="Auckland",
        arrivalAirport="Queenstown",
        regionCode="South Island"
    )

    international1 = InternationalFlight(
        flightNumber="NZ456",
        departureAirport="Auckland",
        arrivalAirport="Sydney",
        countryCode="AU",
        visaRequirement="Visitor visa may be required"
    )

    hybrid1 = HybridFlight(
        flightNumber="NZ789",
        departureAirport="Queenstown",
        arrivalAirport="Singapore",
        regionCode="South Island",
        countryCode="SG",
        visaRequirement="Transit visa may be required",
        isConnecting=True,
        transitAirport="Auckland",
        transitVisa="Required"
    )

    print(domestic1.schedule_flight())
    print(domestic1.get_flight_details())
    print(f"Valid Domestic Route = {domestic1.validate_domestic_route()}")
    print(f"Domestic Fee = ${domestic1.calculate_domestic_fee()}")
    print(domestic1.get_route_info())
    print()

    print(international1.schedule_flight())
    print(international1.get_flight_details())
    print(f"Passport Checked = {international1.check_passport()}")
    print(international1.get_terminal_info())
    print(f"Customs Fee = ${international1.calculate_customs_fee()}")
    print()

    print(hybrid1.schedule_flight())
    print(hybrid1.get_flight_details())
    print(hybrid1.process_transit())
    print(hybrid1.update_manifest())
    print(f"Total Cost = ${hybrid1.calculate_total_cost()}")
    print(HybridFlight.mro())
    print(hybrid1.get_terminal_info())
    print(hybrid1.get_route_info())
