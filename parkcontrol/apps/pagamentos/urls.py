# apps/pagamentos/urls.py

from django.urls import path
from . import views

app_name = 'pagamentos'

urlpatterns = [
    path('clientes-ativos/', views.listar_clientes_ativos, name='listar_clientes_ativos')
]