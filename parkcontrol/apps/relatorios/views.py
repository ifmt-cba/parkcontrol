import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import RelatorioFinanceiro
from .forms import FormularioRelatorioFinanceiro
from apps.pagamentos.models import CobrancaMensalista
from apps.pagamentos.models import CobrancaDiaria
from django.db.models import Sum

logger = logging.getLogger('relatorios')

def relatorios(request):
    logger.info(f"Usuário {request.user} acessou a página principal de relatórios.")
    return render(request, 'relatorios.html')

@login_required
def listar_relatorios(request):
    logger.info(f"Usuário {request.user} listou os relatórios financeiros.")
    relatorios = RelatorioFinanceiro.objects.all().order_by('-editado_em')
    return render(request, 'relatorios/listar.html', {'relatorios': relatorios})

@login_required
def visualizar_relatorio(request, id):
    relatorio = get_object_or_404(RelatorioFinanceiro, pk=id)
    logger.info(f"Usuário {request.user} visualizou o relatório ID={relatorio.id}.")
    return render(request, 'relatorios/visualizar.html', {'relatorio': relatorio})

@login_required
def criar_relatorio(request):
    if request.method == 'POST':
        form = FormularioRelatorioFinanceiro(request.POST)
        if form.is_valid():
            rel = form.save(commit=False)
            rel.criado_por = request.user
            rel.editado_em = timezone.now()

            data_inicio = rel.data_inicio
            data_fim = rel.data_fim

            mensal_emitido = CobrancaMensalista.objects.filter(
                data_geracao__range=(data_inicio, data_fim)
            ).aggregate(total=Sum('valor_devido'))['total'] or 0

            mensal_pago = CobrancaMensalista.objects.filter(
                data_pagamento__range=(data_inicio, data_fim), status='pago'
            ).aggregate(total=Sum('valor_pago'))['total'] or 0

            diaria_emitido = CobrancaDiaria.objects.filter(
                data__range=(data_inicio, data_fim)
            ).aggregate(total=Sum('valor_total'))['total'] or 0

            diaria_pago = CobrancaDiaria.objects.filter(
                data__range=(data_inicio, data_fim), status='Pago'
            ).aggregate(total=Sum('valor_total'))['total'] or 0

            total_emitido = mensal_emitido + diaria_emitido
            total_pago = mensal_pago + diaria_pago
            total_inadimplente = total_emitido - total_pago

            rel.total_emitido = total_emitido
            rel.total_pago = total_pago
            rel.total_inadimplente = total_inadimplente

            rel.save()
            logger.info(f"Usuário {request.user} criou relatório ID={rel.id} de {data_inicio} até {data_fim}.")
            messages.success(request, "Relatório criado com sucesso.")
            return redirect('relatorios:listar')
    else:
        form = FormularioRelatorioFinanceiro()
    return render(request, 'relatorios/criar.html', {'form': form})

@login_required
def editar_relatorio(request, id):
    relatorio = get_object_or_404(RelatorioFinanceiro, pk=id)

    if request.method == 'POST':
        form = FormularioRelatorioFinanceiro(request.POST, instance=relatorio)
        if form.is_valid():
            rel = form.save(commit=False)
            rel.editado_em = timezone.now()
            rel.arquivo_pdf = relatorio.arquivo_pdf
            rel.save()
            logger.info(f"Usuário {request.user} editou relatório ID={rel.id}.")
            messages.success(request, "Relatório atualizado com sucesso.")
            return redirect('relatorios:visualizar', id=rel.id)
    else:
        form = FormularioRelatorioFinanceiro(instance=relatorio)

    return render(request, 'relatorios/editar.html', {'form': form, 'relatorio': relatorio})

@login_required
def excluir_relatorio(request, id):
    relatorio = get_object_or_404(RelatorioFinanceiro, pk=id)
    if request.method == 'POST':
        relatorio.delete()
        logger.warning(f"Usuário {request.user} excluiu relatório ID={id}.")
        messages.success(request, "Relatório excluído com sucesso.")
        return redirect('relatorios:listar')
    return render(request, 'relatorios/excluir.html', {'relatorio': relatorio})