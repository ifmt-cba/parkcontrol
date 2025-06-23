# apps/pagamentos/urls.py

from django.urls import path
from .views import views 
from .views import views_cobrancaDiaria


app_name = 'pagamentos'

urlpatterns = [
    # URLs Gerais (do views.py principal)
    path('gerenciar/', views.gerenciamento_pagamentos_home, name='gerenciamento_pagamentos_home'),
    path('recibo/<str:tipo_cobranca_str>/<int:cobranca_id>/', views.emitir_recibo, name='emitir_recibo'),
    path('listagem-geral-redirect/', views.listagem_pagamentos_geral_redirect, name='listagem_pagamentos_geral_redirect'),
    # URLs de Mensalistas (do views.py principal)
    path('mensalistas/gerar-por-cliente/', views.gerar_pagamentos_mensalistas_lista_clientes, name='gerar_pagamentos_mensalistas_lista_clientes'),
    path('mensalistas/gerar-manual/<int:cliente_id>/', views.gerar_pagamentos_mensalistas_manual, name='gerar_pagamentos_mensalistas_manual'),
    path('mensalistas/cobranca-gerada/<int:cobranca_id>/', views.cobranca_gerada_confirmacao, name='cobranca_gerada_confirmacao'),
    path('mensalistas/', views.listar_cobrancas_mensalistas, name='listar_cobrancas_mensalistas'),
    path('mensalistas/<int:cobranca_id>/', views.detalhe_cobranca_mensalista, name='detalhe_cobranca_mensalista'),
    path('mensalistas/<int:cobranca_id>/editar-status/', views.editar_cobranca_mensalista_status, name='editar_cobranca_mensalista_status'),
    path('mensalistas/disparar-email/<int:cobranca_id>/', views.disparar_email_cobranca, name='disparar_email_cobranca'),

    # Diarista
    path('listar/', views_cobrancaDiaria.listar_cobrancas, name='listar_cobranca'),
    path('atualizar/<int:cobranca_id>/', views_cobrancaDiaria.atualizar_status_cobranca, name='atualizar_status'),
    path('recibo/<int:cobranca_id>/', views_cobrancaDiaria.emitir_recibo, name='emitir_recibo'),
    ]