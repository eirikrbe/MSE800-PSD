
# main_menu.py

from cli.input_helpers import ask_int, ask_text
from cli.display_helpers import (
    clear_screen,
    pause,
    display_title,
    display_success,
    display_error
    )

def main_menu(auth_service):
    """Top-level CLI loop handling login and registration."""
    while True:
        clear_screen()
        display_title("Welcome to Ako-puku \n  Login & Signup Demo")
        print()
        print("1. Login")
        print("2. Register as student (ākonga)")
        print("0. Exit")

        choice = ask_int("\nSelect an option: ")

        if choice == 1:
            clear_screen()
            display_title("Login to Your Account")

            user_email = ask_text("Enter your email: ")
            password = ask_text("Enter your password: ")

            logged_in_user = auth_service.login(user_email, password)

            if logged_in_user:
                display_success(f"Welcome back, {logged_in_user.full_name}! (role: {logged_in_user.role})")
                pause()
            else:
                display_error("Invalid email or password. Please try again.")
                pause()

        elif choice == 2:
            clear_screen()
            display_title("Create Student (ākonga) Account")

            try:
                full_name = ask_text("Full Name: ")
                email = ask_text("Email: ")
                password = ask_text("Password: ")
                phone = ask_text("Phone Number: ")

                registered_user = auth_service.register_user(
                    full_name,
                    email,
                    password,
                    phone=phone
                )

                if registered_user:
                    display_success(
                        f"Registration successful! Welcome, {full_name}. "
                        "Your customer account has been created."
                    )
                    pause()

            except ValueError as e:
                display_error(str(e))
                pause()

        elif choice == 0:
            display_success("Goodbye!")
            pause()
            break

        else:
            display_error("Invalid option. Please try again.")
            pause()
