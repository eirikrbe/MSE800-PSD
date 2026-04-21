
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
        students.append(name)
        age = input(f"Enter the age of student {i + 1}: ")
        students.append(age)
        student_number = input(f"Enter the student ID of student {i + 1}: ")
        students.append(student_number)

        student = Student()
        student.set_data(name, age, student_number)
        students.append(student)

        print() ## empty space


def display_students():
    print("\nStudent Information:")

    sorted_students = sorted(students, key=lambda s: s.name)

    for student in sorted_students:
        print(student.display_data())

if __name__ == "__main__":
    get_info_students()
    display_students()