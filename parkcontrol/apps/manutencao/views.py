from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.usuarios.views.views_autenticacao import is_administrador
from django.contrib import messages
from apps.vagas.models import SolicitacaoManutencao, Vaga
from django.db.models import Q

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

    context = {
        'solicitacoes': solicitacoes,
        'vagas': vagas
    }
    return render(request, 'manutencao/visualizar_solicitacoes.html', context)


def encerrar_solicitacao(request, solicitacao_id):
    solicitacao = get_object_or_404(SolicitacaoManutencao, id=solicitacao_id)

    if solicitacao.resolvido:
        messages.warning(request, "Essa solicitação já foi encerrada.")
    else:
        solicitacao.resolvido = True
        solicitacao.save()

        # Atualiza o status da vaga para "Livre"
        vaga = solicitacao.numero_vaga  # Aqui já é um objeto Vaga
        if vaga.status == "Manutenção":
            vaga.status = "Livre"
            vaga.save()

        messages.success(request, f"A solicitação da vaga {vaga.numero} foi encerrada e a vaga está disponível novamente.")

    return redirect('manutencao:manutencao_dashboard')

def alterar_status_vaga(request, vaga_id):
    if request.method == 'POST':
        novo_status = request.POST.get('status')
        vaga = get_object_or_404(Vaga, id=vaga_id)
        if novo_status in ['Livre', 'Ocupada', 'Manutenção']:
            vaga.status = novo_status
            vaga.save()
            messages.success(request, f"Status da vaga {vaga.numero} alterado para {novo_status}.")
        else:
            messages.error(request, "Status inválido.")
    return redirect('manutencao:manutencao_dashboard')
