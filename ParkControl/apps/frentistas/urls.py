from django.urls import path
from . import views  # Importa as suas views do app frentistas

urlpatterns = [
    path('', views.home_frentista, name='home_frentista'),
    path('gerenciar-clientes/', views.gerenciar_clientes_view, name='gerenciar_clientes'),
]
