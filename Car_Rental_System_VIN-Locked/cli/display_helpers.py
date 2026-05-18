
#display_helpers.py

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


def display_cars(cars, fleet_manager=None):
    if not cars:
        print("No cars available at the moment.")
        return False
    
    if fleet_manager:
        print("\nID | Make / Model | Year | Mileage | Rate | Rent Window | Score")
    else:
        print("\nID | Make / Model | Year | Mileage | Rate | Rent Window")
    
    for car in cars:
        row = (
            f"{car['car_id']} | {car['make']} {car['model']} | "
            f"{car['year']} | {car['mileage']} km | "
            f"${car['daily_rate']:.2f}/day | "
            f"{car['min_rent_period']}-{car['max_rent_period']} days"
        )
        if fleet_manager:
            score = fleet_manager.calculate_confidence_score(car["car_id"])
            row += f" | ⭐ {score}/100"
        print(row)
    
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