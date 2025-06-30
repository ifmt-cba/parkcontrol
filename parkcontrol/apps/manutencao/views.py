import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.usuarios.views.views_autenticacao import is_administrador
from django.contrib import messages
from apps.vagas.models import SolicitacaoManutencao, Vaga
from django.db.models import Q

logger = logging.getLogger('manutencao')  # logger para o app manutencao

def manutencao_dashboard(request):
    filtro_vaga = request.GET.get('vaga')
    filtro_data = request.GET.get('data')
    filtro_protocolo = request.GET.get('protocolo')

    solicitacoes = SolicitacaoManutencao.objects.filter(resolvido=False)
    
    if filtro_vaga:
        solicitacoes = solicitacoes.filter(numero_vaga__icontains=filtro_vaga)
    if filtro_data:
        solicitacoes = solicitacoes.filter(data_solicitacao__date=filtro_data)
    if filtro_protocolo:
        solicitacoes = solicitacoes.filter(id__icontains=filtro_protocolo)

    solicitacoes = solicitacoes.order_by('-data_solicitacao')
    vagas = Vaga.objects.all().order_by('numero')

    logger.info(
        f"Dashboard manutenção acessado com filtros: vaga='{filtro_vaga}', data='{filtro_data}', protocolo='{filtro_protocolo}'. "
        f"{solicitacoes.count()} solicitações não resolvidas listadas."
    )

    context = {
        'solicitacoes': solicitacoes,
        'vagas': vagas
    }
    return render(request, 'manutencao/visualizar_solicitacoes.html', context)


def encerrar_solicitacao(request, solicitacao_id):
    solicitacao = get_object_or_404(SolicitacaoManutencao, id=solicitacao_id)

    if solicitacao.resolvido:
        messages.warning(request, "Essa solicitação já foi encerrada.")
        logger.warning(f"Tentativa de encerrar solicitação já resolvida: ID={solicitacao_id}")
    else:
        solicitacao.resolvido = True
        solicitacao.save()

        # Atualiza o status da vaga para "Livre"
        vaga = solicitacao.numero_vaga  # objeto Vaga
        if vaga.status == "Manutenção":
            vaga.status = "Livre"
            vaga.save()

        messages.success(request, f"A solicitação da vaga {vaga.numero} foi encerrada e a vaga está disponível novamente.")
        logger.info(f"Solicitação ID={solicitacao_id} encerrada. Vaga {vaga.numero} status alterado para Livre.")

    return redirect('manutencao:manutencao_dashboard')


def alterar_status_vaga(request, vaga_id):
    if request.method == 'POST':
        novo_status = request.POST.get('status')
        vaga = get_object_or_404(Vaga, id=vaga_id)
        if novo_status in ['Livre', 'Ocupada', 'Manutenção']:
            status_antigo = vaga.status
            vaga.status = novo_status
            vaga.save()
            messages.success(request, f"Status da vaga {vaga.numero} alterado para {novo_status}.")
            logger.info(f"Status da vaga {vaga.numero} alterado de {status_antigo} para {novo_status} pelo usuário.")
        else:
            messages.error(request, "Status inválido.")
            logger.warning(f"Tentativa de alterar status da vaga {vaga.numero} para valor inválido: {novo_status}")
    return redirect('manutencao:manutencao_dashboard')
