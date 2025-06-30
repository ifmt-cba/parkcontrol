from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from apps.clientes import views

from .views import views_autenticacao, views_dashboard, views_gerencia_usuario, views_perfil, views_gerencia_cliente


app_name = "usuarios"  # Define o namespace para o app usuarios

# URL patterns for the usuarios app
# This file defines the URL patterns for the usuarios app in a Django project.
urlpatterns = [

    # Redirecionamento para a página de login
    path("", views_autenticacao.redirect_to_login, name="redirect_to_login"), # Redirect to login

    # Redirecionamento para a página inicial
    path('home/', views_dashboard.home_redirect, name='home'), # Redirect to home based on user profile

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
    path('editar_usuario/<int:usuario_id>/', views_gerencia_usuario.editar_usuario, name='editar_usuario'),
    path('excluir_usuario/<int:usuario_id>/', views_gerencia_usuario.excluir_usuario, name='excluir_usuario'),

    # perfil
    path('meu_perfil/', views_perfil.perfil_usuario, name='perfil_usuario'),
    path('editar_perfil/', views_perfil.editar_perfil_usuario, name='editar_perfil_usuario'),
    path('alterar_senha/', views_perfil.alterar_senha_usuario, name='alterar_senha_usuario'),

    #esqueceu senha
    
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='autenticacao/password_reset_form.html',
            success_url=reverse_lazy('usuarios:password_reset_done')
        ),
        name='password_reset'
    ),
    path(
        'password_reset_done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='autenticacao/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='autenticacao/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='autenticacao/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    # gerencia de clientes
    path("gerencia_cliente/", views_gerencia_cliente.gerencia_cliente, name='gerencia_cliente'),
    path('mensalistas/', views.cliente_mensalista_view, name='cliente_mensalista'),
    path('diaristas/', views.cliente_diarista_view, name='cliente_diarista'),

]
