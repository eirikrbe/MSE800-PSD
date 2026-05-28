
from factory import DeviceFactory



class DeviceManager:

    _instance = None

    '''
    Singleton implementation: ensures only one DeviceManager instance exists during runtime.
    '''

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    '''
    __init__ may run every time DeviceManager() is called, so _initialized prevents resetting the device list.
    '''
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.devices = []
            self._initialized = True

    
    def add_device(self, device_location, device_type):
        device = DeviceFactory.create_device(device_location, device_type)
        self.devices.append(device)
        return device
    

    def get_devices(self):
        return self.devices
    
    def get_device(self, index):
        if index < 0 or index >= len(self.devices):
            raise ValueError("Invalid device index")
        return self.devices[index]

