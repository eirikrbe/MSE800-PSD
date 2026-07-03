from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='index'),
    path('hello/<str:name>/', views.hello, name='hello'),
    path('fruits/', views.fruits, name='fruits'),
]