from functools import wraps

'''
def function_decorator(func):

    def wrap_function():
        print("first")
        func()
        print("third")

    return wrap_function

@function_decorator
def decorator():
    print("second")
'''

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def hello():
    """This greets."""
    print("hello")

print(hello.__name__)
print(hello.__doc__)

if __name__ == "__main__":
    hello()
    print(hello.__name__)
    print(hello.__doc__)