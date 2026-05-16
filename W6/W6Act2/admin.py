
#admin.py


from decorator_zoo import login_checker


@login_checker
def admin(username, password):
    '''
    user = admin
    password = admin
    '''
    if username == "admin" and password == "admin":
        return True
    return False
