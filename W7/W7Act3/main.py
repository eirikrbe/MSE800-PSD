


from manager import DeviceManager
from models import SmartLight, SmartFan, SmartAirConditioner
import os

def main():
   
    manager = DeviceManager()
    manager2 = DeviceManager()

    print(manager)
    print(manager2)

    print(manager is manager2)

    '''
    Converts menu choices into factory device type keys.
    '''

    device_choice_map = {
        "1": "light",
        "2": "fan",
        "3": "aircon"
        }

    while True:
        os.system("clear")
        print()
        print("Welcome to the Office IoT Management System")
        print()
        print("1. Add Smart Device")
        print("2. Display Device Status")
        print("3. Configure Device")
        print("4. Exit")

        choice = input("\nSelect an option: ").strip()


        if choice == "1":

            print()
            print("Add Smart Device")
            print()
            print("1. Smart Light")
            print("2. Smart Fan")
            print("3. Smart Air Conditioner")

            device_choice = input("\nSelect an option: ").strip()

            if device_choice in device_choice_map:
                device_type = device_choice_map[device_choice]
                device_location = input("Enter device location:")
                device = manager.add_device(device_location, device_type)
                print(f"Smart {device_type} created successfully.")
            else: 
                print("Invalid option")
                continue

        elif choice == "2":

            devices = manager.get_devices()

            if not devices:
                print("No devices created yet")

                input("\nPress Enter to continue...")

            else:
                print("\nDevice | Location | Power | Status")
                print("---------------------------------------------")
                for device in devices:
                    status = device.display_status()
                    row = (
                        f"{status['device']} | {status['location']} | {status['power']} | {status['status']}"
                    )
                    print(row)
                input("\nPress Enter to continue...")

        elif choice == "3":

            devices = manager.get_devices()

            if not devices:
                print("No devices created yet")

            else:
                print("\nID | Device | Location | Power | Status")
                print("---------------------------------------------")
                for index, device in enumerate(devices):
                    status = device.display_status()
                    row = (
                        f"{index} | {status['device']} | {status['location']} | {status['power']} | {status['status']}"
                    )
                    print(row)

                try: 
                    edit_device = int(input("Enter the Device id to edit: "))
                except ValueError:
                    print("Invalid number")
                    continue

                try:
                    selected_device = manager.get_device(edit_device)
                except ValueError as error:
                    print(error)
                    continue

                print("Configure Device")
                print()
                print("1. Turn On")
                print("2. Turn Off")
                print("3. Adjust Setting")

                choice_edition = input("Select Configure Option: ")

                if choice_edition == "1":
                    try:
                        selected_device.turn_on()
                    except ValueError as error:
                        print(error)
                        continue
                
                elif choice_edition == "2":
                    try:
                        selected_device.turn_off()
                    except ValueError as error:
                        print(error)
                        continue

                elif choice_edition == "3":
                    if isinstance(selected_device, SmartLight):
                        try:
                            brightness = int(input("Enter brightness between 0 and 100: "))
                            selected_device.set_brightness(brightness)
                            print("Brightness updated successfully.")
                        except ValueError as error:
                            print(error)    

                    elif isinstance(selected_device, SmartFan):
                        try:
                            speed = input("Enter speed: low, medium, or high: ")
                            selected_device.set_speed(speed)
                            print("Speed updated successfully.")
                        except ValueError as error:
                            print(error)

                    elif isinstance(selected_device, SmartAirConditioner):
                        try:
                            temperature = int(input("Enter temperature between 15 and 32: "))
                            selected_device.set_temperature(temperature)
                            print("Temperature updated successfully.")
                        except ValueError as error:
                            print(error)

        elif choice == "4":
            print("Goodbye.")
            break

if __name__ == "__main__":
    main()