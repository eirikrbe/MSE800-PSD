from models import SmartLight, SmartFan, SmartAirConditioner



class DeviceFactory:

    '''
    Maps user-friendly device type keys to concrete device classes, avoiding a long if/elif creation chain.
    '''

    device_map = {
        "light": SmartLight,
        "fan": SmartFan,
        "aircon": SmartAirConditioner
    }

    @staticmethod
    def create_device(device_location, device_type):

        if device_type not in DeviceFactory.device_map:
            raise ValueError(f"{device_type} is not an allowed type of device")
        device_class = DeviceFactory.device_map[device_type]
        return device_class(device_location)