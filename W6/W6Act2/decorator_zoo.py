
#decorator_zoo.py

from functools import wraps


def login_checker(func):


    @wraps(func)
    def wrapper(*args, **kwargs):
        login_result = func(*args, **kwargs)
        if login_result is True:
            print("Welcome admin")
            return True
        print("Login Failed")    
        return False 
    return wrapper

