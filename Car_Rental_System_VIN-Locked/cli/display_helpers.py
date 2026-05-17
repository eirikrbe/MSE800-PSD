
import os
import platform

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def pause():
    input("\nPress Enter to continue...")

def display_title(title):
    print("\n========================================")
    print(f"  {title}")
    print("========================================")


def display_success(message):
    print(f"\n[SUCCESS] {message}")


def display_error(message):
    print(f"\n[ERROR] {message}")


def display_info(message):
    print(f"\n[INFO] {message}")


def display_available_cars(cars):
    if not cars:
        display_info("No cars available at the moment.")
        return False
    print()
    print("\nAvailable Cars:")
    print()
    print("ID | Make / Model | Year | Mileage | Rate | Status | Rent Window")

    for car in cars:
        print(
            f"{car['car_id']} | {car['make']} {car['model']} | {car['year']} | "
            f"{car['mileage']} km | ${car['daily_rate']:.2f}/day | "
            f"{car['status']} | {car['min_rent_period']}-{car['max_rent_period']} days"
        )

    return True


def display_bookings(bookings, fleet_manager, title="Bookings"):
    if not bookings:
        display_info(f"No {title.lower()} found.")
        return False
    print()
    print(f"\n{title}")
    print()
    print("ID | Car | Dates | Status | Fee")

    for booking in bookings:
        car = fleet_manager.get_car_by_id(booking["car_id"])
        print(
            f"{booking['booking_id']} | {car['make']} {car['model']} | "
            f"{booking['start_date']} → {booking['end_date']} | "
            f"{booking['status']} | ${booking['total_fee']:.2f}"
        )

    return True