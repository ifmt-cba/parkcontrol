from django.urls import path
from . import views

app_name = 'relatorios'

urlpatterns = [
    path('', views.relatorios, name='dashboard_relatorios'),
    path('listar/', views.listar_relatorios, name='listar'),
    path('criar/', views.criar_relatorio, name='criar'),
    path('visualizar/<int:id>/', views.visualizar_relatorio, name='visualizar'),
    path('editar/<int:id>/', views.editar_relatorio, name='editar'),
    path('excluir/<int:id>/', views.excluir_relatorio, name='excluir'),
]
