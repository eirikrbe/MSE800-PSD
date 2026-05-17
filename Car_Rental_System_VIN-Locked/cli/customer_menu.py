
#customer_menu.py


from cli.input_helpers import ask_int, ask_date
from cli.display_helpers import (
    clear_screen,
    pause,
    display_title,
    display_success,
    display_error,
    display_available_cars,
    display_bookings
)

def customer_menu(logged_in_user, auth_service, booking_service, fleet_manager):
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
            display_available_cars(available_cars)
            pause()


        elif choice == 2:
            try:
                clear_screen()
                available_cars = fleet_manager.get_available_cars()

                if not display_available_cars(available_cars):
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
                bookings = booking_service.get_customer_bookings(logged_in_user.user_id)
                display_bookings(bookings, fleet_manager, "My Bookings")
                pause()

            except ValueError as e:
                display_error(f"Error retrieving bookings: {e}")
                pause()
                continue


        elif choice == 4:
            try:
                bookings = booking_service.get_customer_bookings(logged_in_user.user_id)

                if not display_bookings(bookings, fleet_manager, "My Bookings"):
                    pause()
                    continue

                booking_id = ask_int("\nEnter the booking ID to cancel: ")

                if booking_id not in [b["booking_id"] for b in bookings]:
                    display_error(f"Booking ID {booking_id} is not in your bookings.")
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