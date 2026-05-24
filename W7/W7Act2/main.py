from aquarium_manager import AquariumManager


def ask_for_quantity():
    while True:
        try:
            quantity = int(input("Quantity currently available: "))
            if quantity < 0:
                print("Quantity cannot be negative.")
                continue
            return quantity
        except ValueError:
            print("Please enter a whole number.")


def display_inventory(manager):
    print("\nAuckland Aquarium Inventory")
    print("---------------------------")

    inventory = manager.get_fish_inventory()
    if not inventory:
        print("No fish registered yet.")
    else:
        for fish in inventory:
            print(fish.fish())

    print("\nCategory Summary")
    print("----------------")
    for row in manager.get_category_summary():
        print(f"{row['category']}: {row['total']} fish")


def main():
    manager = AquariumManager()
    valid_fish = ", ".join(manager.get_available_fish_names())

    try:
        while True:
            print("\nAuckland Aquarium Manager")
            print("1. Add or update fish")
            print("2. Display inventory")
            print("3. Exit")

            option = input("Choose an option: ").strip()

            if option == "1":
                name = input(f"Fish name ({valid_fish}): ").strip()
                quantity = ask_for_quantity()
                try:
                    fish = manager.save_fish(name, quantity)
                    print(f"Saved: {fish.fish()}")
                except ValueError as error:
                    print(error)
            elif option == "2":
                display_inventory(manager)
            elif option == "3":
                print("Closing Auckland Aquarium Manager.")
                break
            else:
                print("Choose option 1, 2, or 3.")
    finally:
        manager.close_connection()


if __name__ == "__main__":
    main()
