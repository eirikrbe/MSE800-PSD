

#customer_menu.py

from cli.input_helpers import ask_int, ask_date

def customer_menu(logged_in_user, auth_service, booking_service, fleet_manager):
    while True:
        print("\n========================================")
        print("  Customer Menu")
        print("========================================")
        print("1. View Available Cars")
        print("2. Make a Booking")
        print("3. View My Bookings")
        print("4. Request Cancellation")
        print("0. Logout")

        choice = ask_int("\nSelect an option: ")

        if choice == 1:
            available_cars = fleet_manager.get_available_cars()
            if available_cars:
                print("\nAvailable Cars:")
                print("ID | Make / Model | Year | Mileage | Rate | Status | Rent Window")
                for car in available_cars:
                    print(
                        f"{car['car_id']} | {car['make']} {car['model']} | {car['year']} | "
                        f"{car['mileage']} km | ${car['daily_rate']:.2f}/day | {car['status']} | "
                        f"{car['min_rent_period']}-{car['max_rent_period']} days"
                    )
            else:
                print("No cars available at the moment.")

        elif choice == 2:
            try:
                available_cars = fleet_manager.get_available_cars()
                if available_cars:
                    print("\nAvailable Cars:")
                    print("ID | Make / Model | Year | Mileage | Rate | Status | Rent Window")
                    for car in available_cars:
                        print(
                            f"{car['car_id']} | {car['make']} {car['model']} | {car['year']} | "
                            f"{car['mileage']} km | ${car['daily_rate']:.2f}/day | {car['status']} | "
                            f"{car['min_rent_period']}-{car['max_rent_period']} days"
                        )
                else:
                    print("No cars available at the moment.")
                    continue

                print("\n========================================")
                print("\nEnter booking details:")
                print("\n========================================")

                car_id = ask_int("Enter car ID: ")
                start_date = ask_date("Enter start date (YYYY-MM-DD): ")
                end_date = ask_date("Enter end date (YYYY-MM-DD): ")

                booking_id = booking_service.request_booking(
                    logged_in_user.user_id,
                    car_id,
                    start_date,
                    end_date
                )

                print(f"Booking request created successfully. Booking ID: {booking_id}")

            except ValueError as e:
                print(f"Booking failed: {e}")
                continue


        elif choice == 0:
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")