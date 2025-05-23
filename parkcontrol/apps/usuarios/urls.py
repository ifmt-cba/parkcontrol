from django.urls import path
from . import views

# URL patterns for the usuarios app
# This file defines the URL patterns for the usuarios app in a Django project.
urlpatterns = [
    path("", views.redirect_to_login, name="redirect_to_login"), # Redirect to login
    path("home/", views.home_parkcontrol, name="home_parkcontrol"), # Home page
    path("login/", views.login_parkcontrol, name="login_parkcontrol"), # Login page 
    path('register/', views.register_parkcontrol, name='register_parkcontrol'), # Registration page
    path("logout/", views.logout_parkcontrol, name="logout_parkcontrol"), # Logout page
]
