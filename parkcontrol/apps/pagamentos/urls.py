# apps/pagamentos/urls.py

from django.urls import path
from . import views

app_name = 'pagamentos'

urlpatterns = [
    path('gerenciar/', views.gerenciamento_pagamentos_home, name='gerenciamento_pagamentos_home'),
    path('mensalistas/gerar-por-cliente/', views.gerar_pagamentos_mensalistas_lista_clientes, name='gerar_pagamentos_mensalistas_lista_clientes'),
    path('mensalistas/gerar-manual/<int:cliente_id>/', views.gerar_pagamentos_mensalistas_manual, name='gerar_pagamentos_mensalistas_manual_com_cliente'),
    path('mensalistas/gerar-imediata/<int:cliente_id>/', views.gerar_cobranca_imediata, name='gerar_cobranca_imediata'),
    path('listagem-geral-redirect/', views.listagem_pagamentos_geral_redirect, name='listagem_pagamentos_geral_redirect'),
    path('movimento/<int:movimento_id>/encerrar/', views.registrar_saida_e_cobrar, name='registrar_saida_e_cobrar'),
    path('diarista/<int:cobranca_id>/pagar/', views.registrar_pagamento_diarista, name='registrar_pagamento_diarista'),
    path('diaristas/', views.listar_cobrancas_diaristas, name='listar_cobrancas_diaristas'),
    path('diaristas/<int:cobranca_id>/', views.detalhe_cobranca_diarista, name='detalhe_cobranca_diarista'),
    path('diaristas/<int:cobranca_id>/editar-status/', views.editar_cobranca_diarista_status, name='editar_cobranca_diarista_status'),
    path('diaristas/<int:cobranca_id>/excluir/', views.excluir_cobranca_diarista, name='excluir_cobranca_diarista'),
    path('mensalistas/', views.listar_cobrancas_mensalistas, name='listar_cobrancas_mensalistas'),
    path('mensalistas/<int:cobranca_id>/', views.detalhe_cobranca_mensalista, name='detalhe_cobranca_mensalista'),
    path('mensalistas/<int:cobranca_id>/editar-status/', views.editar_cobranca_mensalista_status, name='editar_cobranca_mensalista_status'),
    path('mensalistas/<int:cobranca_id>/excluir/', views.excluir_cobranca_mensalista, name='excluir_cobranca_mensalista'),
    path('mensalistas/enviar-email-lista/', views.listar_cobrancas_para_email, name='listar_cobrancas_para_email'),
    path('mensalistas/disparar-email/<int:cobranca_id>/', views.disparar_email_cobranca, name='disparar_email_cobranca'),
    path('cobranca-gerada/<int:cobranca_id>/', views.cobranca_gerada_confirmacao, name='cobranca_gerada_confirmacao'),
    path('recibo/<str:tipo_cobranca_str>/<int:cobranca_id>/', views.emitir_recibo, name='emitir_recibo'),
]