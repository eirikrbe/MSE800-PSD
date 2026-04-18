

def get_info_students():
    students = []
    print("How many students are there?")
    num_students = int(input())
    for i in range(num_students):
        name = input(f"Enter the name of student {i + 1}: ")
        students.append(name)
        age = input(f"Enter the age of student {i + 1}: ")
        students.append(age)
        student_number = input(f"Enter the student ID of student {i + 1}: ")
        students.append(student_number)
    return students

def display_students(students):
    print("\nStudent Information:")
    new_list = sorted(students)
    for i in range(0, len(new_list), 3):
        print(f"Name: {new_list[i]}, Age: {new_list[i + 1]}, Student ID: {new_list[i + 2]}")

def main():
    print("Week 2 – Activity 2: Student Information")
    students = get_info_students()
    display_students(students)

if __name__ == "__main__":
    main()