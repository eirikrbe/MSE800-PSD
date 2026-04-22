
# Week 2 – Activity 3: OOP mathematical operations

class Calculator:
    """A single mathematical operation on two operands.

        Attributes:
        a: First operand (float or complex).
        b: Second operand (float or complex).
        operator: One of +, -, *, /, %.
        _result: private attribute, stores the result of the calculation.
    """

    def __init__(self, a, b, operator):
        self.a = a
        self.b = b
        self.operator = operator
        self._result = None ## Store the result of the calculation after execution. read via the result property.

    def _validate_operation(self):
        """Validate the operation before execution.

            Raises:
            ZeroDivisionError: If b is zero and operator is / or %.
            TypeError: If operator is % and either operand is complex.
        """

        if self.operator == "/" and self.b == 0:
            raise ZeroDivisionError("Error: Division by zero is not allowed.")
        if self.operator == "%" and self.b == 0:
            raise ZeroDivisionError("Error: Modulo by zero is not allowed.")
        if self.operator == "%" and (isinstance(self.a, complex) or isinstance(self.b, complex)):
            raise TypeError("Error: Modulo operation is not supported for complex numbers.")

    def calculate(self):
        """Validate and execute the operation.

            Returns:
            float | complex: Result of the operation.

            Raises:
            ZeroDivisionError: If b is zero and operator is / or %.
            TypeError: If operator is % and either operand is complex.
            ValueError: If operator is not recognized.
        """

        self._validate_operation()
        
        if self.operator == "+":
            self._result = self.a + self.b
            return self._result
        elif self.operator == "-":
            self._result = self.a - self.b
            return self._result
        elif self.operator == "*":
            self._result = self.a * self.b
            return self._result
        elif self.operator == "/":
            self._result = self.a / self.b
            return self._result
        elif self.operator == "%":
            self._result = self.a % self.b
            return self._result
        raise ValueError(f"Unsupported operator: {self.operator}")
    
    def __str__(self):
        """Returns the operation as a string for display purposes."""
        
        return f"{self.a} {self.operator} {self.b}"
    
    @property
    def result(self):
        """Returns the result of the operation, if calculated."""
        
        if self._result is None:
            raise ValueError("Operation has not been calculated yet.")
        return self._result
    

def get_number_kind():
    while True:
            choice = input("Do you want to work with real numbers (r) or complex numbers (c)?: ").lower()
            if choice in ("r", "c"):
                return choice
            print("Invalid input. Please enter 'r' for real numbers or 'c' for complex numbers.") 
                

def get_operator():
    while True:
        operator = input("Enter the operator (+, -, *, /, %): ")
        if operator in ("+", "-", "*", "/", "%"):
            return operator
        print("Invalid operator. Please enter one of the following: +, -, *, /, %.")
            

def get_number(number, kind):
    """Read a number and convert it according with its kind previously selected."""

    while True:
        try:
            value = input(f"Enter number {number}: ")
            if kind == "r":
                return float(value)
            elif kind == "c":
                return complex(value)
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def main():
        
        print()
        print("Week 2 – Activity 3: OOP mathematical operations")
        print()

        kind = get_number_kind()
        a = get_number("a", kind)
        b = get_number("b", kind)
        operator = get_operator()

        operation = Calculator(a, b, operator)
        
        try:

            result = operation.calculate()
            print()
            print(f"The result of {operation} is {result}.")
            print()

        except (ZeroDivisionError, TypeError, ValueError) as e:
            print(e)
        

if __name__ == "__main__":
    while True:
        main()
        again = input("Do you want to perform another calculation? (y/n): ").lower()
        if again != "y":
            print()
            break