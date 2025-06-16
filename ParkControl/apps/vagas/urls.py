from django.urls import path
from . import views

app_name = 'vagas'

urlpatterns = [
    path('entrada/', views.registrar_entrada_view, name='registrar_entrada'),
    path('buscar-nome/', views.buscar_nome_por_placa, name='buscar_nome_por_placa'),
    path('saida/', views.registrar_saida_view, name='registrar_saida'),
    path('buscar-saida/', views.buscar_saida_por_placa, name='buscar_saida_por_placa'),
    path('solicitar-manutencao/', views.solicitar_manutencao, name='solicitar_manutencao'),
    path('relatorio/', views.relatorio_uso_vagas, name='relatorio_uso'),
    path('status/', views.status_vagas_view, name='status_vagas'),
    path('api/status-vagas/', views.api_status_vagas, name='api_status_vagas'),
]
