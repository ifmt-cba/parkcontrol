from django.urls import path
from . import views

app_name = 'manutencao'

urlpatterns = [
    path('painel/', views.manutencao_dashboard, name='manutencao_dashboard'),
    path('solicitacoes/<int:solicitacao_id>/encerrar/', views.encerrar_solicitacao, name='encerrar_solicitacao'),
    path('alterar-status-vaga/<int:vaga_id>/', views.alterar_status_vaga, name='alterar_status_vaga'),
]
