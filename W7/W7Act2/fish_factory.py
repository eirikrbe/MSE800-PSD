from abc import ABC, abstractmethod


class Fish(ABC):
    """Base product for every fish in the aquarium."""

    def __init__(self, name, quantity, category):
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.name = name.title()
        self.quantity = quantity
        self.category = category

    @abstractmethod
    def fish(self):
        pass


class FreshwaterFish(Fish):
    """Concrete product for freshwater fish."""

    def __init__(self, name, quantity):
        super().__init__(name, quantity, "Freshwater")

    def fish(self):
        return f"{self.name} | Category: {self.category} | Quantity: {self.quantity}"


class SaltwaterFish(Fish):
    """Concrete product for saltwater fish."""

    def __init__(self, name, quantity):
        super().__init__(name, quantity, "Saltwater")

    def fish(self):
        return f"{self.name} | Category: {self.category} | Quantity: {self.quantity}"


class FishFactory:
    """Factory responsible for creating Fish objects."""

    def create_fish(self, name, quantity, category):
        fish_name = name.strip().lower()
        fish_category = category.strip().title()

        if fish_category == "Freshwater":
            return FreshwaterFish(fish_name, quantity)

        if fish_category == "Saltwater":
            return SaltwaterFish(fish_name, quantity)

        raise ValueError("Fish category must be Freshwater or Saltwater.")
