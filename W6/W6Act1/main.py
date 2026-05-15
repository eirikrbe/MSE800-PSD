from users import (
    student_login,
    submit_assignment,
    view_grades
)


def main():
    '''
    This function runs the main program by calling the decorated user functions.
    Each function triggered the log_activity decorator before and after the original function executed
    '''

    student_login("Mohammad")

    submit_assignment(
        "Mohammad",
        "Python Decorator Project"
    )

    view_grades("Mohammad")


if __name__ == "__main__":
    main()
