from Land import get_input, RegularLand

    
def main():
        
        print()
        print("Week 4 – Activity 2: OOP mathematical operations")
        print()
   
        length = get_input("Enter the length of the land: ")
        width = get_input("Enter the width of the land: ")

        land = RegularLand(length, width)
        print(f"The area of the land is: {land.area()}")    
        print(f"The perimeter of the land is: {land.perimeter()}")

if __name__ == "__main__":
    while True:
        main()
        again = input("Do you want to perform another calculation? (y/n): ").lower()
        if again != "y":
            print()
            break