
# Auckland aquarium inventory using OOP, Factory, Singleton, and SQLite.


import sqlite3
from abc import ABC, abstractmethod
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent / "aquarium.db"


class Fish(ABC):
    """Abstract parent class for all fish species."""

    @abstractmethod
    def species(self):
        pass

    @abstractmethod
    def category(self):
        pass


# Each species is also mapped to a general aquarium category.


class Goldfish(Fish):
    def species(self):
        return "Goldfish"

    def category(self):
        return "Freshwater"


class Shark(Fish):
    def species(self):
        return "Shark"

    def category(self):
        return "Saltwater"


class Angelfish(Fish):
    def species(self):
        return "Angelfish"

    def category(self):
        return "Freshwater"


class Tuna(Fish):
    def species(self):
        return "Tuna"

    def category(self):
        return "Saltwater"


class Salmon(Fish):
    def species(self):
        return "Salmon"

    def category(self):
        return "Freshwater"


class FishFactory:
    """Factory Pattern: creates fish objects from species names."""

    fish_classes = {
        "goldfish": Goldfish,
        "shark": Shark,
        "angelfish": Angelfish,
        "tuna": Tuna,
        "salmon": Salmon,
    }

    def create_fish(self, species_name):
        fish_class = self.fish_classes.get(species_name.lower())
        if fish_class is None:
            raise ValueError(f"{species_name} is not available in this aquarium.")

        return fish_class()

    def available_species(self):
        return list(self.fish_classes.keys())


class Aquarium:
    """Singleton Pattern: one shared aquarium database manager."""

    _instance = None

    def __new__(cls, database_path=DATABASE_PATH):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.database_path = database_path
            cls._instance.connection = None

        if cls._instance.connection is None:
            cls._instance.connection = sqlite3.connect(cls._instance.database_path)
            cls._instance.create_table()

        return cls._instance

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS fish_stock (
                species TEXT PRIMARY KEY,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL
            )
            """
        )
        self.connection.commit()

    def set_fish_quantity(self, fish, quantity):
        species = fish.species()
        category = fish.category()
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO fish_stock (species, category, quantity)
            VALUES (?, ?, ?)
            ON CONFLICT(species)
            DO UPDATE SET
                category = excluded.category,
                quantity = excluded.quantity
            """,
            (species, category, quantity),
        )
        self.connection.commit()

    def get_stock(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT species, category, quantity FROM fish_stock ORDER BY species"
        )
        return cursor.fetchall()

    def display_stock(self):
        stock = self.get_stock()
        if not stock:
            print("No fish are currently available in the aquarium.")
            return

        print("\nAuckland Aquarium Fish Stock")
        print("---------------------------")
        for species, category, quantity in stock:
            print(f"{species} ({category}): {quantity}")

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None


def read_quantity(fish):
    while True:
        species = fish.species()
        category = fish.category()
        user_input = input(
            f"Enter current number of {species} ({category}), or press Enter to skip: "
        ).strip()

        if user_input == "":
            return None

        try:
            quantity = int(user_input)
            if quantity < 0:
                print("Please enter zero or a positive number.")
                continue
            return quantity
        except ValueError:
            print("Please enter a valid number.")


def main():
    factory = FishFactory()
    aquarium = Aquarium()

    print("Auckland Aquarium Management System")
    print("Press Enter to skip a fish and keep its current database value.\n")

    try:
        for species_name in factory.available_species():
            fish = factory.create_fish(species_name)
            quantity = read_quantity(fish)
            if quantity is not None:
                aquarium.set_fish_quantity(fish, quantity)

        aquarium.display_stock()
    finally:
        aquarium.close()


if __name__ == "__main__":
    main()
