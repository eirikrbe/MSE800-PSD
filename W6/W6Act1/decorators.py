from datetime import datetime



def log_activity(func):
    '''
    This is the decorator of the program, its purpose to call and display the decorated functions
    '''

    def wrapper(*args, **kwargs):
        '''
        this's a the inner function which gives behavio r to the program
        '''
        print("===================================")
        print(f"Function: {func.__name__}")
        print(f"Time: {datetime.now()}")
        print("Activity started...")

        result = func(*args, **kwargs)

        print("Activity completed.")
        print("===================================\n")

        return result

    return wrapper
