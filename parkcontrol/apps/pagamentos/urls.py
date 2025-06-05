# apps/pagamentos/urls.py

from django.urls import path
from . import views

app_name = 'pagamentos'

urlpatterns = [
     # --- Home do Módulo de Gerenciamento de Pagamentos (Contador) ---
    path('gerenciar/', views.gerenciamento_pagamentos_home, name='gerenciamento_pagamentos_home'),
    
    # --- URL para a tela de "Clientes Ativos" que será usada para Gerar Pagamentos ---
    path('mensalistas/gerar-por-cliente/', views.gerar_pagamentos_mensalistas_lista_clientes, name='gerar_pagamentos_mensalistas_lista_clientes'),
    
    # --- URL para o FORMULÁRIO de geração de cobrança manual ---
    path('mensalistas/gerar-manual/<int:cliente_id>/', views.gerar_pagamentos_mensalistas_manual, name='gerar_pagamentos_mensalistas_manual_com_cliente'),
    path('mensalistas/gerar-manual/', views.gerar_pagamentos_mensalistas_manual, name='gerar_pagamentos_mensalistas_manual'),
]