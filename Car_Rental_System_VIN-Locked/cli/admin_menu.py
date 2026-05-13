
#admin_menu.py

from cli.input_helpers import ask_int, ask_date, ask_text

def admin_menu(logged_in_user, auth_service, booking_service, fleet_manager):
    print("\n========================================")
    print("  Admin Menu")
    print("========================================")
    print("1. Add New Car to Fleet")
    print("2. View All Bookings")
    print("0. Logout")  

