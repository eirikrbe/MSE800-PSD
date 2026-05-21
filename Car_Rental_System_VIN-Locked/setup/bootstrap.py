
#bootstrap.py

from datetime import date, timedelta
from database.booking_queries import add_booking
from database.car_queries import update_car_status


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
    ("SEEDVIN006", "Tesla", "Model 3", 2024, 5000, 90.00, 1, 7, 30, 10),
]

def make_booking_data(customer_id, car, start_offset, end_offset, status):
    start = date.today() + timedelta(days=start_offset)
    end = date.today() + timedelta(days=end_offset)

    duration = (end - start).days
    total_fee = duration * car["daily_rate"]

    return (
        customer_id,
        car["car_id"],
        start.strftime("%Y-%m-%d"),
        end.strftime("%Y-%m-%d"),
        total_fee,
        status
    )


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
    demo_car1 = fleet_manager.get_car_by_vin(cars[0][0])
    demo_car2 = fleet_manager.get_car_by_vin(cars[1][0])
    demo_car3 = fleet_manager.get_car_by_vin(cars[2][0])
    demo_car4 = fleet_manager.get_car_by_vin(cars[3][0])
    demo_car5 = fleet_manager.get_car_by_vin(cars[4][0])
    demo_car6 = fleet_manager.get_car_by_vin(cars[5][0])


    seed_bookings = [
        make_booking_data(demo_customer["user_id"], demo_car1, 3, 6, "pending"),
        make_booking_data(demo_customer["user_id"], demo_car2, 7, 10, "approved"),
        make_booking_data(demo_customer["user_id"], demo_car3, -1, 3, "active"),
        make_booking_data(demo_customer["user_id"], demo_car4, 12, 16, "cancelled"),
        make_booking_data(demo_customer["user_id"], demo_car5, -20, -15, "completed"),
        make_booking_data(demo_customer["user_id"], demo_car5, -10, -7, "completed"),
        make_booking_data(demo_customer["user_id"], demo_car6, 18, 20, "rejected"),
    ]


    if not booking_service.booking_exists():
        for booking in seed_bookings:
            customer_id, car_id, start_date, end_date, total_fee, status = booking

            add_booking(
                booking_service.db_manager,
                customer_id,
                car_id,
                start_date,
                end_date,
                total_fee,
                status
            )

            if status in ["pending", "approved"]:
                new_status = "locked"
            elif status == "active":
                new_status = "rented"
            else:
                new_status = "available"

            update_car_status(booking_service.db_manager, car_id, new_status)

        created["booking"] = True

    return created