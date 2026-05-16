# W6 Activity 2 - Zoo Admin Login System

## Overview

This project is a simple admin login system for a Zoo Application. It is designed for an admin user and exists to demonstrate how a Python decorator can separate login checking from the main program flow.

## Project Structure

```text
zoo_admin_login/
│
├── decorator_zoo.py   ← contains the login checker decorator
├── admin.py           ← contains the admin login function
├── main.py            ← runs the program and repeats login until successful
└── README.md
```

## How To Run

The program will ask for a username and password. Enter the correct admin credentials to access the system.

Default credentials:
```text
Username: admin
Password: admin
```

## File Responsibilities

### `decorator_zoo.py`

This file contains the login_checker decorator. It exists to check whether the login attempt was successful without putting that checking logic directly inside main.py.

### `admin.py`

This file contains the admin() function. It exists to receive the username and password, compare them with the correct admin credentials, and return True or False.

### `main.py`

This file runs the application. It asks the user to enter their username and password, calls the decorated admin() function, and repeats the login process until the correct details are entered.

## Key Concept

The project uses `@wraps(func)` to preserve the original function’s name and documentation. This keeps the decorated function easier to understand and avoids Python treating it only as the internal wrapper() function.