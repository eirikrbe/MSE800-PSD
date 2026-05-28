from abc import ABC, abstractmethod

class SmartDevice(ABC): 

    def __init__(self, device_location):
       
        self.device_location = device_location
        self.power_status = "OFF"

    def turn_on(self):

        if self.power_status != "OFF":
            raise ValueError (f"The {self.device_location} is already ON")
        self.power_status = "ON"
    
    def turn_off(self):

        if self.power_status != "ON":
            raise ValueError (f"The {self.device_location} is already OFF")
        self.power_status = "OFF"

    '''
    Forces each smart device subclass to provide its own status format while sharing common power behaviour.
    '''
        
    @abstractmethod
    def display_status(self) -> dict[str, str]:
        pass

class SmartLight(SmartDevice):

    def __init__(self, device_location, brightness_level=50):

        super().__init__(device_location)
        self.brightness_level = brightness_level

    def display_status(self) -> dict[str, str]:
        return {
                    "device": "Smart Light",
                    "location": self.device_location,
                    "power": self.power_status,
                    "status": (f"brightness = {self.brightness_level}%")
                }
    
    def set_brightness(self, brightness):
        if brightness < 0 or brightness > 100:
            raise ValueError("Value needs to be between 0 and 100")
        self.brightness_level = brightness

    
class SmartFan(SmartDevice):

    def __init__(self, device_location, speed_level="Medium"):

        super().__init__(device_location)
        self.speed_level = speed_level

    def display_status(self) -> dict[str, str]:
        return {
                    "device": "Smart Fan",
                    "location": self.device_location,
                    "power": self.power_status,
                    "status": (f"speed = {self.speed_level}")
                }
    
    def set_speed(self, speed):
        if speed.lower() not in ["low", "medium", "high"]:
            raise ValueError("Value needs to be low or medium or high")
        self.speed_level = speed


class SmartAirConditioner(SmartDevice):

    def __init__(self, device_location, temperature=22):

        super().__init__(device_location)
        self.temperature = temperature
    
    def display_status(self) -> dict[str, str]:
        return {
                    "device": "Smart Air Conditioner",
                    "location": self.device_location,
                    "power": self.power_status,
                    "status": (f"temperature = {self.temperature}°C")
                }
    
    def set_temperature(self, temperature):
        if temperature < 15 or temperature > 32:
            raise ValueError("Value needs to be between 15 and 32")
        self.temperature = temperature

    