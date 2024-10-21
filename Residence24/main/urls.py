# main/urls.py
from django.contrib import admin
from django.urls import path, include
from main.views import home, about, contact


app_name ='main'

urlpatterns = [
    path('home/', home, name='home'),  # URL for the home page
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
]