from django.urls import path
from . import views  # Importa as suas views do app frentistas

app_name = 'frentistas'  # isso é necessário para usar o namespace

urlpatterns = [
    path('gerenciar-clientes/', views.gerenciar_clientes_view, name='gerenciar_clientes'),
    path('gerenciar-vagas/', views.gerenciar_vagas_view, name='gerenciar_vagas'),
]
