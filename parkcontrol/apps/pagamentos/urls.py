# apps/pagamentos/urls.py

from django.urls import path
from . import views

app_name = 'pagamentos'

urlpatterns = [
    path('gerenciar/', views.gerenciamento_pagamentos_home, name='gerenciamento_pagamentos_home'),
    
    # URL para a lista de clientes Mensalistas
    path('mensalistas/gerar-por-cliente/', views.gerar_pagamentos_mensalistas_lista_clientes, name='gerar_pagamentos_mensalistas_lista_clientes'),
    
    # URL para a nova view de geração imediata
    path('mensalistas/gerar-imediata/<int:cliente_id>/', views.gerar_cobranca_imediata, name='gerar_cobranca_imediata'),

    # URL para a tela de confirmação de cobrança gerada
    path('mensalistas/cobranca-gerada/<int:cobranca_id>/', views.cobranca_gerada_confirmacao, name='cobranca_gerada_confirmacao'),

    # --- URLs para as cobranças de Mensalistas ---
    path('mensalistas/', views.listar_cobrancas_mensalistas, name='listar_cobrancas_mensalistas'),
    path('mensalistas/<int:cobranca_id>/', views.detalhe_cobranca_mensalista, name='detalhe_cobranca_mensalista'),
    path('mensalistas/<int:cobranca_id>/editar-status/', views.editar_cobranca_mensalista_status, name='editar_cobranca_mensalista_status'),
    path('mensalistas/<int:cobranca_id>/excluir/', views.excluir_cobranca_mensalista, name='excluir_cobranca_mensalista'),

    # --- URLs para as cobranças de Diaristas ---
    path('diaristas/gerar-por-cliente/', views.gerar_pagamentos_diaristas_lista_clientes, name='gerar_pagamentos_diaristas_lista_clientes'),
    path('diaristas/gerar-movimento/<int:diarista_id>/', views.gerar_movimento_diarista_imediata, name='gerar_movimento_diarista_imediata'),
    path('diaristas/', views.listar_cobrancas_diaristas, name='listar_cobrancas_diaristas'),
    path('diaristas/<int:cobranca_id>/', views.detalhe_cobranca_diarista, name='detalhe_cobranca_diarista'),
    path('diaristas/<int:cobranca_id>/editar-status/', views.editar_cobranca_diarista_status, name='editar_cobranca_diarista_status'),
    path('diaristas/<int:cobranca_id>/excluir/', views.excluir_cobranca_diarista, name='excluir_cobranca_diarista'),
    
    # URL para emitir recibo 
    path('recibo/<str:tipo_cobranca_str>/<int:cobranca_id>/', views.emitir_recibo, name='emitir_recibo'),

    # URLs de e-mail
    path('mensalistas/enviar-email-lista/', views.listar_cobrancas_para_email, name='listar_cobrancas_para_email'),
    path('mensalistas/disparar-email/<int:cobranca_id>/', views.disparar_email_cobranca, name='disparar_email_cobranca'),
]