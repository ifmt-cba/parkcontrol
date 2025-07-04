from django.shortcuts import render
import logging
from django.contrib.auth.decorators import login_required

logger = logging.getLogger('usuarios')

@login_required(login_url='login_parkcontrol')
def gerencia_cliente(request):
    logger.info(f"Usuário {request.user.username} acessou a tela de gerenciamento de clientes.")
    return render(request, 'usuarios/administrador/gerencia_cliente.html')
