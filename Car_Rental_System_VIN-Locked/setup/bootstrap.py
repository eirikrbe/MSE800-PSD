
#bootstrap.py

from datetime import date, timedelta

admin = {
    "full_name": "System Admin",
    "email": "admin",
    "password": "admin",
    "phone": None,
    "role": "admin"
}

customer = {
    "full_name": "System Customer",
    "email": "customer",
    "password": "customer",
    "phone": None,
    "role": "customer"
}

cars = [
    ("SEEDVIN001", "Toyota", "Corolla", 2021, 20000, 50.00, 1, 30, 20, 1),
    ("SEEDVIN002", "Mazda", "Axela", 2019, 62000, 55.00, 1, 21, 12, 3),
    ("SEEDVIN003", "Honda", "Civic", 2020, 48000, 60.00, 2, 28, 8, 1),
    ("SEEDVIN004", "Nissan", "X-Trail", 2022, 35000, 85.00, 2, 30, 15, 0),
    ("SEEDVIN005", "Suzuki", "Swift", 2018, 70000, 45.00, 1, 14, 10, 4),
]

def run_app_setup(auth_service, fleet_manager, booking_service):

    created = {
        "admin": False,
        "customer": False,
        "cars": False,
        "booking": False
    }
    
    if not auth_service.admin_exists():
        auth_service.register_user(**admin)
        created["admin"] = True
    
    if not auth_service.user_exists("customer"):
        auth_service.register_user(**customer)
        created["customer"] = True

    for car in cars:
        car_data = car[:8]
        attempts = car[8]
        conflicts = car[9]

        vin = car_data[0]

        if not fleet_manager.car_exists_by_vin(vin):
            fleet_manager.add_car(*car_data)

            created_car = fleet_manager.get_car_by_vin(vin)

            fleet_manager.update_car_booking_statistics(
                created_car["car_id"],
                attempts,
                conflicts
            )

            created["cars"] = True
    
    demo_customer = auth_service.get_user_by_email("customer")
    demo_car = fleet_manager.get_car_by_vin(cars[0][0])

    start_date = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    end_date = (date.today() + timedelta(days=5)).strftime("%Y-%m-%d")

    if not booking_service.booking_exists():
        booking_service.request_booking(
            demo_customer["user_id"],
            demo_car["car_id"],
            start_date,
            end_date
        )
        created["booking"] = True
    
    

    return created