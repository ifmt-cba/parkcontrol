from django.urls import path
from .views import views_autenticacao, views_dashboard, views_gerencia_usuario

# URL patterns for the usuarios app
# This file defines the URL patterns for the usuarios app in a Django project.
urlpatterns = [
    path("", views_autenticacao.redirect_to_login, name="redirect_to_login"), # Redirect to login

    # autenticacao
    path("login/", views_autenticacao.login_parkcontrol, name="login_parkcontrol"), # Login page 
    path("logout/", views_autenticacao.logout_parkcontrol, name="logout_parkcontrol"), # Logout page


    # dashboard
    path("dashboard_administrador/", views_dashboard.dashboard_administrador, name="dashboard_administrador"), # Dashboard for Administrador
    path("dashboard_frentista/", views_dashboard.dashboard_frentista, name="dashboard_frentista"), # Dashboard for Frentista
    path("dashboard_contador/", views_dashboard.dashboard_contador, name="dashboard_contador"), # Dashboard for Contador

    # gerencia de usuarios
    path("gerencia_usuarios/", views_gerencia_usuario.gerencia_usuarios, name="gerencia_usuarios"), # Manage usuarios
    path('register/', views_gerencia_usuario.register_parkcontrol, name='register_parkcontrol'), # Registration page
]
