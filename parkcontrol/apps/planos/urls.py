from django.urls import path
from . import views

app_name = 'planos'

urlpatterns = [

    path('selecao/', views.selecao_plano, name='selecao_plano'),

    path('planos/mensais/', views.listar_planos_mensais, name='listar_planos_mensais'),
    path('planos/diarios/', views.listar_planos_diarios, name='listar_planos_diarios'),

    path('planos/mensais/novo/', views.criar_plano_mensal, name='criar_plano_mensal'),
    path('planos/diarios/novo/', views.criar_plano_diario, name='criar_plano_diario'),

    path('planos/mensais/editar/<int:id>/', views.editar_plano_mensal, name='editar_plano_mensal'),
    path('planos/diarios/editar/<int:id>/', views.editar_plano_diario, name='editar_plano_diario'),

    path('planos/mensais/visualizar/<int:id>/', views.visualizar_plano_mensal, name='visualizar_plano_mensal'),
    path('planos/diarios/visualizar/<int:id>/', views.visualizar_plano_diario, name='visualizar_plano_diario'),

    path('planos/mensais/excluir/<int:id>/', views.excluir_plano_mensal, name='excluir_plano_mensal'),
    path('planos/diarios/excluir/<int:id>/', views.excluir_plano_diario, name='excluir_plano_diario'),

]
