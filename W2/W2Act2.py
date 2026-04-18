
from turtle import st


students = []

class Student:
    def set_data(self, name, age, student_number):
        self.name = name
        self.age = age
        self.student_number = student_number

    def display_data(self):
        return f"Name: {self.name}, Age: {self.age}"


def get_info_students():
    
    print("How many students?")
    num_students = int(input())

    for i in range(num_students):
        name = input(f"Enter the name of student {i + 1}: ")
        age = input(f"Enter the age of student {i + 1}: ")
        student_number = input(f"Enter the student ID of student {i + 1}: ")

        student = Student()
        student.set_data(name, age, student_number)
        students.append(student)

        print()

def display_students(students):
    print("\nStudent Information:")
    new_list = sorted(students, key=lambda s: s.age)

    for student in new_list:
        print(student.display_data())


if __name__ == "__main__":
    get_info_students()
    display_students(students)