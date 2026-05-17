
#admin_menu.py


from cli.input_helpers import ask_int, ask_float, ask_text
from cli.display_helpers import (
    clear_screen,
    pause,
    display_title,
    display_success,
    display_error,
    display_bookings
)


def admin_menu(logged_in_user, auth_service, booking_service, fleet_manager):
    while True:
        clear_screen()
        display_title("Admin Menu")
        print("1. View pending bookings")
        print("2. Approve booking")
        print("3. Reject booking")
        print("4. Activate booking")
        print("5. Complete booking")
        print("6. Add car")
        print("7. Update car")
        print("8. Delete car")
        print("0. Logout")

        choice = ask_int("\nSelect an option: ")

        if choice == 1:
            clear_screen()
            bookings = booking_service.get_bookings_by_status("pending")
            display_bookings(bookings, fleet_manager, "Pending Bookings")
            pause()

        elif choice == 2:
            try:
                clear_screen()
                bookings = booking_service.get_bookings_by_status("pending")

                if not display_bookings(bookings, fleet_manager, "Pending Bookings"):
                    pause()
                    continue

                booking_id = ask_int("\nEnter the booking ID to approve: ")
                booking_service.process_booking_approval(booking_id)
                display_success(f"Booking ID {booking_id} approved.")
            except ValueError as e:
                display_error(str(e))
            pause()

        elif choice == 3:
            try:
                clear_screen()
                bookings = booking_service.get_bookings_by_status("pending")

                if not display_bookings(bookings, fleet_manager, "Pending Bookings"):
                    pause()
                    continue

                booking_id = ask_int("\nEnter the booking ID to reject: ")
                booking_service.process_booking_rejection(booking_id)
                display_success(f"Booking ID {booking_id} rejected.")
            except ValueError as e:
                display_error(str(e))
            pause()

        elif choice == 4:
            try:
                clear_screen()
                bookings = booking_service.get_bookings_by_status("approved")

                if not display_bookings(bookings, fleet_manager, "Approved Bookings"):
                    pause()
                    continue

                booking_id = ask_int("\nEnter the booking ID to activate: ")
                booking_service.process_booking_activation(booking_id)
                display_success(f"Booking ID {booking_id} activated.")
            except ValueError as e:
                display_error(str(e))
            pause()

        elif choice == 5:
            try:
                clear_screen()
                bookings = booking_service.get_bookings_by_status("active")

                if not display_bookings(bookings, fleet_manager, "Active Bookings"):
                    pause()
                    continue

                booking_id = ask_int("\nEnter the booking ID to complete: ")
                booking_service.process_booking_completion(booking_id)
                display_success(f"Booking ID {booking_id} completed.")
            except ValueError as e:
                display_error(str(e))
            pause()

        elif choice == 6:
            try:
                clear_screen()
                display_title("Add New Car")

                vin = ask_text("VIN: ")
                make = ask_text("Make: ")
                model = ask_text("Model: ")
                year = ask_int("Year: ")
                mileage = ask_int("Mileage: ")
                daily_rate = ask_float("Daily rate: ")
                min_rent_period = ask_int("Minimum rent period: ")
                max_rent_period = ask_int("Maximum rent period: ")

                car_id = fleet_manager.add_car(
                    vin,
                    make,
                    model,
                    year,
                    mileage,
                    daily_rate,
                    min_rent_period,
                    max_rent_period
                )

                display_success(f"Car added successfully. Car ID: {car_id}")
                pause()

            except ValueError as e:
                display_error(str(e))
                pause()

        elif choice == 0:
            display_success("Goodbye!")
            break

        else:
            display_error("Invalid option. Please try again.")
            pause()
