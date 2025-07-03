from django.shortcuts import render
from django.template.loader import get_template
import logging

logger = logging.getLogger('frentistas')

def gerenciar_vagas_view(request):
    logger.info(f"Usuário {request.user.username} acessou a tela de gerenciamento de vagas.")

    # 🔍 TESTE: Verifica se o template existe
    get_template('frentistas/gerenciar_vagas.html')  # Lança erro se não encontrar

    return render(request, 'frentistas/gerenciar_vagas.html')
