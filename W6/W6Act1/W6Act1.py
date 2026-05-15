

def function_decorator(func):

    def wrap_function():
        print("first")
        func()
        print("third")

    return wrap_function

@function_decorator
def decorator():
    print("second")


if __name__ == "__main__":
    
    decorator()