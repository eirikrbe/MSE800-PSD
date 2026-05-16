
#main.py

from admin import admin


def main():
    while True:

        user = input("insert user:  ")
        password = input("insert pass:  ")
      
        login = admin(user, password)
        
        if login:
            break


if __name__ == "__main__":

    main()