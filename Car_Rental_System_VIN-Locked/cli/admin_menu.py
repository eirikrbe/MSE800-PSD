
#admin_menu.py


from cli.input_helpers import ask_int, ask_float, ask_text
from cli.display_helpers import (
    clear_screen,
    display_info,
    pause,
    display_title,
    display_success,
    display_error,
    display_bookings,
    display_cars
)

def admin_menu(auth_service, booking_service, fleet_manager):
    while True:
        clear_screen()
        display_title("Admin Menu")
        print("1. View pending bookings")
        print("2. Approve booking")
        print("3. Reject booking")
        print("4. Activate booking")
        print("5. Complete booking")
        print("6. Cancel booking")
        print("7. Add car")
        print("8. Update car")
        print("9. Delete car")
        print("10. Register user as a Admin")
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

                pending_bookings = booking_service.get_bookings_by_status("pending")
                approved_bookings = booking_service.get_bookings_by_status("approved")

                cancellable_bookings = pending_bookings + approved_bookings

                if not display_bookings(
                    cancellable_bookings,
                    fleet_manager,
                    "Bookings Available for Cancellation"
                ):
                    pause()
                    continue

                booking_id = ask_int("\nEnter the booking ID to cancel: ")

                if booking_id not in [b["booking_id"] for b in cancellable_bookings]:
                    display_error(f"Booking ID {booking_id} is not available for cancellation.")
                    pause()
                    continue

                booking_service.process_booking_cancellation(booking_id)

                display_success(f"Booking ID {booking_id} cancelled successfully.")

  
            except ValueError as e:
                display_error(str(e))
            pause()


        elif choice == 7:
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


        elif choice == 8:
            try:
                clear_screen()
                display_title("Update Car")
                cars = fleet_manager.get_all_cars()

                if not display_cars(cars, fleet_manager):
                    pause() 
                    continue    

                car_id = ask_int("\nEnter the Car ID to Update: ")

                make = input("New make (press Enter to skip): ").strip() or None
                model = input("New model (press Enter to skip): ").strip() or None
                year_input = input("New year (press Enter to skip): ").strip()
                year = int(year_input) if year_input else None
                mileage_input = input("New mileage (press Enter to skip): ").strip()
                mileage = int(mileage_input) if mileage_input else None
                daily_rate_input = input("New daily rate (press Enter to skip): ").strip()
                daily_rate = float(daily_rate_input) if daily_rate_input else None
                min_rent_input = input("New minimum rent period (press Enter to skip): ").strip()
                min_rent_period = int(min_rent_input) if min_rent_input else None
                max_rent_input = input("New maximum rent period (press Enter to skip): ").strip()
                max_rent_period = int(max_rent_input) if max_rent_input else None

                if not any([make, model, year, mileage, daily_rate, min_rent_period, max_rent_period]):
                    display_error("No fields to update.")
                    pause()
                    continue                
                
                fleet_manager.update_car(
                    car_id,
                    make=make,
                    model=model,
                    year=year,
                    mileage=mileage,
                    daily_rate=daily_rate,
                    min_rent_period=min_rent_period,
                    max_rent_period=max_rent_period
                )

                display_success(f"Car ID {car_id} updated successfully.")

            except ValueError as e:
                display_error(str(e))
            pause()


        elif choice == 9:
            try:
                clear_screen()  
                display_title("Deleting a Car")
                cars = fleet_manager.get_all_cars()

                if not display_cars(cars, fleet_manager):
                    pause() 
                    continue    

                car_id = ask_int("\nEnter the Car ID to delete: ")
                delete_option = input(f"Are you sure you want to delete car ID {car_id}? (y/n): ").strip().lower()

                if delete_option == "y":
                    fleet_manager.delete_car(car_id)
                    display_success(f"Car ID {car_id} deleted successfully.")
                    pause()
                elif delete_option == "n":
                    display_info("Delete cancelled.")
                    pause()
                else:
                    display_error("Invalid option. Delete cancelled.")
                    pause()
  
            except ValueError as e:
                display_error(str(e))
            pause()


        elif choice == 10:
            clear_screen()
            display_title("Create Admin Account")

            try:
                full_name = ask_text("Full Name: ")
                email = ask_text("Email: ")
                password = ask_text("Password: ")
                phone = ask_text("Phone Number: ")

                registered_user = auth_service.register_user(
                    full_name,
                    email,
                    password,
                    phone=phone,
                    role="admin"
                )

                if registered_user:
                    display_success(
                        f"Registration successful! Welcome, {full_name}. "
                        "Your Admin account has been created."
                    )
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
