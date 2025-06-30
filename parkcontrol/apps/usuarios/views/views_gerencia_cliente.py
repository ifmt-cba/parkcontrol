from django.shortcuts import render
import logging

logger = logging.getLogger('usuarios')

def gerencia_cliente(request):
    logger.info(f"Usuário {request.user.username} acessou a tela de gerenciamento de clientes.")
    return render(request, 'usuarios/administrador/gerencia_cliente.html')
