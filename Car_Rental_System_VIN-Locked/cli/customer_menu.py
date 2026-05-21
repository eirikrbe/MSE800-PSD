
#customer_menu.py


from cli.input_helpers import ask_int, ask_date
from cli.display_helpers import (
    clear_screen,
    pause,
    display_title,
    display_success,
    display_error,
    display_cars,
    display_bookings
)

def customer_menu(logged_in_user, booking_service, fleet_manager):
    while True:
        clear_screen()
        display_title("Customer Menu")
        print("1. View Available Cars")
        print("2. Make a Booking")
        print("3. View My Bookings")
        print("4. Request Cancellation")
        print("0. Logout")

        choice = ask_int("\nSelect an option: ")

        if choice == 1:
            clear_screen()
            available_cars = fleet_manager.get_available_cars()
            display_title("Available Cars")
            display_cars(available_cars, fleet_manager)
            pause()


        elif choice == 2:
            try:
                clear_screen()
                available_cars = fleet_manager.get_available_cars()
                display_title("Make a Booking")

                if not display_cars(available_cars, fleet_manager):
                    pause() 
                    continue
                
                display_title("Enter Booking Details")

                car_id = ask_int("Enter car ID: ")
                start_date = ask_date("Enter start date (YYYY-MM-DD): ")
                end_date = ask_date("Enter end date (YYYY-MM-DD): ")

                booking_id = booking_service.request_booking(
                    logged_in_user.user_id,
                    car_id,
                    start_date,
                    end_date
                )

                display_success(f"Booking request created successfully. Booking ID: {booking_id}")
                pause()

            except ValueError as e:
                display_error(f"Booking failed: {e}")
                pause()
                continue


        elif choice == 3:
            try:
                clear_screen()
                bookings = booking_service.get_customer_bookings(logged_in_user.user_id)
                display_bookings(bookings, fleet_manager, "My Bookings")
                pause()

            except ValueError as e:
                display_error(f"Error retrieving bookings: {e}")
                pause()
                continue


        elif choice == 4:
            try:
                clear_screen()
                bookings = booking_service.get_customer_bookings(logged_in_user.user_id)

                cancellable_bookings = [booking for booking in bookings if booking["status"] in ["pending", "approved"]]

                if not display_bookings(cancellable_bookings, fleet_manager, "Bookings Available for Cancellation"):
                    pause()
                    continue

                booking_id = ask_int("\nEnter the booking ID to cancel: ")

                if booking_id not in [b["booking_id"] for b in cancellable_bookings]:
                    display_error(f"Booking ID {booking_id} is not available for cancellation")
                    pause()
                    continue

                booking_service.process_booking_cancellation(booking_id)

                display_success(f"Booking ID {booking_id} has been cancelled successfully.")
                pause()

            except ValueError as e:
                display_error(f"Cancellation failed: {e}")
                pause()
                continue

        elif choice == 0:
            display_success("Goodbye!")
            break
        else:
            display_error("Invalid option. Please try again.")
            pause()