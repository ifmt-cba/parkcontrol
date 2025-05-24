from django.urls import path
from . import views

# URL patterns for the usuarios app
# This file defines the URL patterns for the usuarios app in a Django project.
urlpatterns = [
    path("", views.redirect_to_login, name="redirect_to_login"), # Redirect to login

    # autenticacao
    path("login/", views.login_parkcontrol, name="login_parkcontrol"), # Login page 
    path('register/', views.register_parkcontrol, name='register_parkcontrol'), # Registration page
    path("logout/", views.logout_parkcontrol, name="logout_parkcontrol"), # Logout page


    # dashboard
    path("dashboard_administrador/", views.dashboard_administrador, name="dashboard_administrador"), # Dashboard for Administrador
    path("dashboard_frentista/", views.dashboard_frentista, name="dashboard_frentista"), # Dashboard for Frentista
    path("dashboard_contador/", views.dashboard_contador, name="dashboard_contador"), # Dashboard for Contador
]
