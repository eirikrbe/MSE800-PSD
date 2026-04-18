
print("Week 2 – Activity 1: mathematical operations")

def get_numbers():
    while True:
        try:
            choice = input("Do you want to work with real numbers (r) or complex numbers (c)?: ").lower()
            if choice == "r":
                numbera = float(input("Enter number a: "))
                numberb = float(input("Enter number b: "))
            elif choice == "c":
                numbera = complex(input("Enter number a: "))
                numberb = complex(input("Enter number b: "))
            else:
                print("Invalid input. Please enter 'r' for real numbers or 'c' for complex numbers.") 
                continue
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue
        return numbera, numberb

def operations(x, y, operator):
    if operator == "+":
        return x + y
    elif operator == "-":
        return x - y
    elif operator == "*":
        return x * y
    elif operator == "/":
        if y != 0:
            return x / y
        else:
            print("Error: Division by zero is not allowed.")
            return None
    elif operator == "%":
        # Modulo is restricted to real numbers in this calculator.
        if isinstance(x, complex) or isinstance(y, complex):
            print("Error: Modulo operation is not supported for complex numbers.")
            return None
        elif y != 0:
            return x % y
        else:
            print("Error: Division by zero is not allowed.")
            return None
    else:
        print("Invalid operator.")
        return None

def main():
    print("W2 Act 1 - mathematical operations (x,y)")
    
    while True:

        numbera, numberb = get_numbers()

        operator = input("Enter the operator (+, -, *, /, %): ")

        result = operations(numbera, numberb, operator)

        if result is not None:
            print(f"The result of {numbera} {operator} {numberb} is {result}")
            break

while True:
    main()  

    choice = input("Do you want to continue (y/n)?: ").lower()
    if choice != "y":
        print("Program finished.")
        break