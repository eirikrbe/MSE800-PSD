from django.http import HttpResponse

def home(request, username):
    return HttpResponse(f"Welcome, {username} to Django!")


