
#main_menu.py

from cli.admin_menu import admin_menu
from cli.customer_menu import customer_menu
from cli.input_helpers import ask_int, ask_text

def main_menu(auth_service, booking_service, fleet_manager):
    while True:
        print("\n========================================")
        print("  Welcome to Car Rental System")
        print("  VIN-Locked Smart Reservation")
        print("========================================")
        print("1. Login")
        print("2. Register")
        print("0. Exit")
        
        choice = ask_int("\nSelect an option: ")
        
        if choice == 1:
            
            print("\n========================================")
            print("  Login to Your Account")
            print("========================================")
            user_email = ask_text("Enter your email: ")
            password = ask_text("Enter your password: ")

            logged_in_user = auth_service.login(user_email, password)
            if logged_in_user:
                print(f"\nWelcome back, {logged_in_user.full_name}!")
                if logged_in_user.role == 'admin':
                    admin_menu(logged_in_user, auth_service, booking_service, fleet_manager)
                else:
                    customer_menu(logged_in_user, auth_service, booking_service, fleet_manager)
            else:
                print("Invalid email or password. Please try again.")

        elif choice == 2:

            print("\n========================================")
            print("  Create a New Account")
            print("========================================")
            full_name = ask_text("Full Name: ")
            email = ask_text("Email: ")
            password = ask_text("Password: ")
            role = ask_text("Role (customer/admin): ")
            if role not in ['customer', 'admin']:
                print("Invalid role. Please enter 'customer' or 'admin'.")
                continue
            phone = ask_text("Phone Number: ")

            register_user = auth_service.register_user(full_name, email, password, role, phone)
            if register_user:
                print(f"\nRegistration successful! Welcome, {full_name}! as a {role}.")
            else:
                print("Registration failed. Please check your details and try again.")

        elif choice == 0:
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")