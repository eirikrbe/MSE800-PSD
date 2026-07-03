"""
The simplest possible Django app — everything in ONE file.

Run it with:
    python simple.py runserver

Then open any of these in your browser:
    http://127.0.0.1:8000/hello/Eric/
    http://127.0.0.1:8000/about/
    http://127.0.0.1:8000/add/3/5/
"""
import sys

from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpResponse
from django.urls import path

# 1. Settings: the bare minimum Django needs to start.
settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,   # URLs live in THIS file
    ALLOWED_HOSTS=["*"],
)


# 2. Views: each function takes a request and returns a response.
def home(request, username):
    # <str:username> in the URL becomes the "username" argument.
    return HttpResponse(f"Welcome, {username} to Django!")


def about(request):
    # No URL variables, so the view takes only "request".
    return HttpResponse("This is the about page.")


def add(request, a, b):
    # <int:a> and <int:b> arrive as real integers, so we can add them.
    return HttpResponse(f"{a} + {b} = {a + b}")


# 3. URLs: map a web address to a view above. Add a line per route.
urlpatterns = [
    path("hello/<str:username>/", home),   # /hello/Eric/
    path("about/", about),                 # /about/
    path("add/<int:a>/<int:b>/", add),     # /add/3/5/
]


# 4. Entry point: lets you run "python simple.py runserver".
if __name__ == "__main__":
    execute_from_command_line(sys.argv)
