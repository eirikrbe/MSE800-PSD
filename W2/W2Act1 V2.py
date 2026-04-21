
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
    while True:
        try:
            value = input(f"Enter number {number}: ")
            if kind == "r":
                return float(value)
            elif kind == "c":
                return complex(value)
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def validate_operation(x, y, operator):
    if operator == "/" and y == 0:
        return "Error: Division by zero is not allowed."
    
    if operator == "%" and (isinstance(x, complex) or isinstance(y, complex)):
        return "Error: Modulo operation is not supported for complex numbers."
    
    if operator == "%" and y == 0:
        return "Error: Division by zero is not allowed."
    
    return None


def calculate(x, y, operator):
    if operator == "+":
        return x + y
    elif operator == "-":
        return x - y
    elif operator == "*":
        return x * y
    elif operator == "/":
        return x / y
    elif operator == "%":
        return x % y
    return None


def main():   

    print("Week 2 – Activity 1 2.0: mathematical operations")

    kind = get_number_kind()
    x = get_number("a", kind)
    y = get_number("b", kind)
    operator = get_operator()

    validation_error = validate_operation(x, y, operator)
    if validation_error:
        print(validation_error)
        return
    
    result = calculate(x, y, operator)
    print(f"The result of {x} {operator} {y} is {result}")


while True:
    main()  

    choice = input("Do you want to continue (y/n)?: ").lower()
    if choice != "y":
        print("Program finished.")
        break