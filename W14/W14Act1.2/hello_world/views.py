from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def fruits(request):
    return render(request, 'hello_world/fruits.html', context={'fruits': []})


def hello(request, name):
    return render(request, 'hello_world/hello.html', context={'name': name})


def homepage(request):
    return render(request, 'hello_world/index.html', context={'name': 'Eric'})