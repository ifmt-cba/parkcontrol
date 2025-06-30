from django.shortcuts import render
import logging

logger = logging.getLogger('frentistas')

def gerenciar_clientes_view(request):
    logger.info(f"Usuário {request.user.username} acessou a tela de gerenciamento de clientes.")
    return render(request, 'frentistas/gerenciar_clientes.html')


def gerenciar_vagas_view(request):
    logger.info(f"Usuário {request.user.username} acessou a tela de gerenciamento de vagas.")
    return render(request, 'frentistas/gerenciar_vagas.html')


def gerenciar_cobranca_diaria(request):
    logger.info(f"Usuário {request.user.username} acessou a tela de cobrança diária.")
    return render(request, 'frentistas/gerenciar_cobranca_diaria.html')
