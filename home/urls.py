from django.contrib import admin
from django.urls import  path, include
from home import views

app_name = 'home'
urlpatterns = [
    path("", views.index, name='home'),
    path("about", views.about, name='about'),
    path("services", views.services, name='services'),
    path("contact", views.contact, name='contact'),
    path("login", views.loginUser, name='login'),
    path("logout", views.logoutUser, name='logout'),
    path("send_email", views.send_email, name="home")
    # path("ajax/", views.call_validate_emails, name="call_validate_emails"),
] 
