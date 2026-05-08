from abc import ABC, abstractmethod


def get_input(prompt):
    while True:
        try:
            return float(input(prompt))                
        except ValueError:
            print("Invalid input. Please enter a valid number.")


class Land(ABC):
    @abstractmethod 
    def area(self):
        pass
    @abstractmethod
    def perimeter(self):
        pass
        
class RegularLand(Land):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area (self):
        return self.length * self.width
    
    def perimeter(self):
        return 2 * (self.length + self.width)
    
