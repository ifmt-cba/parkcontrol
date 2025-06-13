from django.urls import path
from . import views

app_name = 'vagas'

urlpatterns = [
    path('entrada/', views.registrar_entrada_view, name='registrar_entrada'),
    path('buscar-nome/', views.buscar_nome_por_placa, name='buscar_nome_por_placa'),
    path('saida/', views.registrar_saida_view, name='registrar_saida'),
    path('buscar-saida/', views.buscar_saida_por_placa, name='buscar_saida_por_placa'),
    path('listar-vagas/', views.listar_vagas,name='listar_vagas'),
    path('solicitar-manutencao/', views.solicitar_manutencao, name='solicitar_manutencao'),
]
