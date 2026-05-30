

class Flight:
    '''
    Parent class that has three general attributes and one method that returns the information.
    '''
    def __init__(self, flightNumber, departureAirport, arrivalAirport):
        self.flightNumber = flightNumber
        self.departureAirport = departureAirport
        self.arrivalAirport = arrivalAirport


    def get_flight_details(self):
        return f"Flight Number = {self.flightNumber}, Departure Airport {self.departureAirport}, Arrival Airport {self.arrivalAirport}"
    

class DomesticFlight(Flight):
    '''
    Child class that inherits the attributes of its parent, adds its own attribute, and returns the details.
    '''
    def __init__(self, flightNumber, departureAirport, arrivalAirport, region):
        super().__init__(flightNumber, departureAirport, arrivalAirport)
        self.region = region

    def get_domestic_details(self):
        return f"Domestic Flight Number = {self.flightNumber}, Departure Airport {self.departureAirport}, Arrival Airport {self.arrivalAirport}, Region {self.region}"


if __name__ == "__main__":

    domestic1 = DomesticFlight('abc123', 'Auckland', 'Queenstown', 'south island') 
    print(domestic1.get_domestic_details())