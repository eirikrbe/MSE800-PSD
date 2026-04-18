
# W1 Act 3&4 - Power (x,y)
#Powerxy is a program that calculates the power of a number given a base and an exponent.

def get_float_input(value):
    while True:
        try:
            return float(input(value))
        except ValueError:
            print("Invalid input, please enter a float.")

def powerxy(x, y):
    return x ** y

def main():
    print("W1 Act 3&4 - Power (x,y)")
    
    while True:
        base = get_float_input("Enter the Base: ")
        exp = get_float_input("Enter the Exponent: ")

        ## Prevent undefined operation where base is 0 and exponent is non-positive
        
        if base == 0 and exp <= 0:
            print("Undefined: 0 cannot be raised to a non-positive exponent.")
            continue

        result = powerxy(base, exp)

        print(f"{base} raised to the power of {exp} is {result}")
        break

while True:
    main()  

    choice = input("Do you want to continue (y/n)?: ").lower()
    if choice != "y":
        print("Program finished.")
        break