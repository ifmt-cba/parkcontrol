from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from decimal import Decimal
from datetime import datetime, date
import calendar
import re

from .models import Movimento, ConfiguracaoTarifa, PlanoMensal, ClienteMensalista, CobrancaDiarista, CobrancaMensalista
from .forms import GerarCobrancaMensalForm, CobrancaDiaristaStatusForm, CobrancaMensalistaStatusForm


# --- Views para Frentista (Registrar Saída/Cobrança Avulsa) ---


def registrar_saida_e_cobrar(request, movimento_id):
    movimento = get_object_or_404(Movimento, id=movimento_id)

    if movimento.hora_saida:
        messages.warning(request, "Este movimento já foi encerrado e uma cobrança foi gerada anteriormente.")
        try:
            cobranca_existente = CobrancaDiarista.objects.get(movimento=movimento)
            return redirect('pagamentos:detalhe_cobranca_diarista', cobranca_id=cobranca_existente.id)
        except CobrancaDiarista.DoesNotExist:
            return redirect('alguma_url_detalhe_movimento')


    if request.method == 'POST':
        with transaction.atomic():
            movimento.hora_saida = timezone.now()
            
            valor_a_cobrar = movimento.calcular_total_estacionamento()
            movimento.valor_total_calculado = valor_a_cobrar
            movimento.save()

            cobranca = CobrancaDiarista.objects.create(
                movimento=movimento,
                valor_devido=valor_a_cobrar,
                status='pendente',
                data_vencimento=timezone.now().date()
            )
            messages.success(request, f"Saída registrada e cobrança de R${valor_a_cobrar:.2f} gerada para o veículo {movimento.placa_veiculo}.")
            return redirect('pagamentos:detalhe_cobranca_diarista', cobranca_id=cobranca.id)

    return render(request, 'pagamentos/confirmar_saida.html', {'movimento': movimento})

def registrar_pagamento_diarista(request, cobranca_id):
    cobranca = get_object_or_404(CobrancaDiarista, id=cobranca_id)

    if cobranca.esta_paga():
        messages.info(request, "Esta cobrança já está paga.")
        return redirect('pagamentos:detalhe_cobranca_diarista', cobranca_id=cobranca.id)

    if request.method == 'POST':
        try:
            valor_recebido = Decimal(request.POST.get('valor_recebido', '0').replace(',', '.'))
            if valor_recebido <= 0:
                messages.error(request, "O valor recebido deve ser maior que zero.")
                return render(request, 'pagamentos/registrar_pagamento_diarista.html', {'cobranca': cobranca})
        except Exception as e:
            messages.error(request, f"Valor de pagamento inválido: {e}. Use números e vírgula para decimais.")
            return render(request, 'pagamentos/registrar_pagamento_diarista.html', {'cobranca': cobranca})

        with transaction.atomic():
            resultado_pagamento = cobranca.salvar_pagamento(valor_recebido)
            messages.success(request, resultado_pagamento)
            return redirect('pagamentos:detalhe_cobranca_diarista', cobranca_id=cobranca.id)
    
    return render(request, 'pagamentos/registrar_pagamento_diarista.html', {'cobranca': cobranca})

def gerar_pagamentos_mensalistas_manual(request):
    """
    Gerar Pagamentos Mensalistas (manual pelo contador).
    """
    if request.method == 'POST':
        form = GerarCobrancaMensalForm(request.POST)
        if form.is_valid():
            cliente_mensalista = form.cleaned_data['cliente_mensalista']
            mes_referencia_str = form.cleaned_data['mes_referencia']
            data_vencimento = form.cleaned_data['data_vencimento']
            valor_devido = form.cleaned_data['valor_devido']

            with transaction.atomic():
                CobrancaMensalista.objects.create(
                    cliente_mensalista=cliente_mensalista,
                    mes_referencia=mes_referencia_str,
                    data_vencimento=data_vencimento,
                    valor_devido=valor_devido,
                    status='pendente',
                )
                messages.success(request, f"Cobrança mensal gerada com sucesso para {cliente_mensalista.usuario.get_full_name()} referente a {mes_referencia_str}.")
            return redirect('pagamentos:listar_cobrancas_mensalistas')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    field_name = form[field].label or field
                    messages.error(request, f"Erro no campo '{field_name}': {error}")
            return render(request, 'pagamentos/mensalistas/gerar_pagamentos_mensalistas_manual.html', {'form': form})
    else:
        form = GerarCobrancaMensalForm()

    context = {
        'form': form,
    }
    return render(request, 'pagamentos/mensalistas/gerar_pagamentos_mensalistas_manual.html', context)


# --- Views para Contador (Gerenciamento de Pagamentos) ---


def gerenciamento_pagamentos_home(request):
    """
    Interface principal do módulo Gerenciamento de Pagamentos para o Contador.
    """
    return render(request, 'pagamentos/gerenciamento_pagamentos_home.html')

def listar_clientes_ativos(request):
    """
    Lista clientes/cobranças consideradas ativas.
    Exemplo: lista cobranças pendentes de diaristas e mensalistas.
    """
    
    cobrancas_diaristas_pendentes = CobrancaDiarista.objects.filter(status='pendente').order_by('-data_geracao')
    cobrancas_mensalistas_pendentes = CobrancaMensalista.objects.filter(status='pendente').order_by('-data_geracao')
    
    lista_para_template = []

    for cobranca_d in cobrancas_diaristas_pendentes:
        lista_para_template.append({
            'id': cobranca_d.id,
            'nome_ou_identificador': f"Diarista: {cobranca_d.movimento.placa_veiculo if cobranca_d.movimento else 'N/D'} (ID: {cobranca_d.id})",
            'status_pagamento': cobranca_d.get_status_display(),
            'tipo_cliente': 'Diarista',
            'tipo_cobranca_url': 'diarista'
        })

    for cobranca_m in cobrancas_mensalistas_pendentes:
        lista_para_template.append({
            'id': cobranca_m.id,
            'nome_ou_identificador': f"Mensalista: {cobranca_m.cliente_mensalista.usuario.get_full_name() if cobranca_m.cliente_mensalista and cobranca_m.cliente_mensalista.usuario else 'N/D'} (ID: {cobranca_m.id})",
            'status_pagamento': cobranca_m.get_status_display(),
            'tipo_cliente': 'Mensalista',
            'tipo_cobranca_url': 'mensalista'
        })

    context = {
        'clientes': lista_para_template,
        'titulo_pagina': 'Clientes Ativos / Cobranças Pendentes'
    }
    return render(request, 'gerar_pagamentos/listar_clientes_ativos.html', context)

def listagem_pagamentos_geral_redirect(request):
    """
    View auxiliar para o botão "Visualizar e Editar Pagamentos"
    """
    return redirect('pagamentos:listar_cobrancas_mensalistas') 

def gerar_pagamentos_mensalistas_manual(request):
    """
    Gerar Pagamentos Mensalistas (manual pelo contador).
    """
    if request.method == 'POST':
        form = GerarCobrancaMensalForm(request.POST)
        if form.is_valid():
            cliente_mensalista = form.cleaned_data['cliente_mensalista']
            mes_referencia_str = form.cleaned_data['mes_referencia']
            data_vencimento = form.cleaned_data['data_vencimento']
            valor_devido = form.cleaned_data['valor_devido']

            with transaction.atomic():
                CobrancaMensalista.objects.create(
                    cliente_mensalista=cliente_mensalista,
                    mes_referencia=mes_referencia_str,
                    data_vencimento=data_vencimento,
                    valor_devido=valor_devido,
                    status='pendente',
                )
                messages.success(request, f"Cobrança mensal gerada com sucesso para {cliente_mensalista.usuario.get_full_name()} referente a {mes_referencia_str}.")
            return redirect('pagamentos:listar_cobrancas_mensalistas')
        else:

            for field, errors in form.errors.items():
                for error in errors:
                    field_name = form[field].label or field
                    messages.error(request, f"Erro no campo '{field_name}': {error}")

            return render(request, 'pagamentos/gerar_pagamentos_mensalistas_manual.html', {'form': form})
    else:
        form = GerarCobrancaMensalForm()

    context = {
        'form': form,
    }
    return render(request, 'pagamentos/gerar_pagamentos_mensalistas_manual.html', context)

def detalhe_cobranca_diarista(request, cobranca_id):
    cobranca = get_object_or_404(CobrancaDiarista, id=cobranca_id)
    return render(request, 'pagamentos/detalhe_cobranca_diarista.html', {'cobranca': cobranca})

def editar_status_cobranca_diarista(request, cobranca_id):
    cobranca = get_object_or_404(CobrancaDiarista, id=cobranca_id)
    if request.method == 'POST':
        form = CobrancaDiaristaStatusForm(request.POST)
        if form.is_valid():
            cobranca.status = form.cleaned_data['status']
            if cobranca.status == 'pago' and not cobranca.data_pagamento:
                cobranca.data_pagamento = timezone.now()
                cobranca.valor_pago = cobranca.valor_devido
            cobranca.save()
            messages.success(request, "Status da cobrança de diarista atualizado com sucesso.")
            return redirect('pagamentos:detalhe_cobranca_diarista', cobranca_id=cobranca.id)
    else:
        form = CobrancaDiaristaStatusForm(initial={'status': cobranca.status})
    return render(request, 'pagamentos/editar_status_cobranca_diarista.html', {'form': form, 'cobranca': cobranca})


def detalhe_cobranca_mensalista(request, cobranca_id):
    cobranca = get_object_or_404(CobrancaMensalista, id=cobranca_id)
    return render(request, 'pagamentos/detalhe_cobranca_mensalista.html', {'cobranca': cobranca})

def editar_status_cobranca_mensalista(request, cobranca_id):
    cobranca = get_object_or_404(CobrancaMensalista, id=cobranca_id)
    if request.method == 'POST':
        form = CobrancaMensalistaStatusForm(request.POST)
        if form.is_valid():
            cobranca.status = form.cleaned_data['status']
            # Se o status for 'pago', defina data_pagamento
            if cobranca.status == 'pago' and not cobranca.data_pagamento:
                cobranca.data_pagamento = timezone.now()
                cobranca.valor_pago = cobranca.valor_devido # Assumindo pagamento integral
            cobranca.save()
            messages.success(request, "Status da cobrança de mensalista atualizado com sucesso.")
            return redirect('pagamentos:detalhe_cobranca_mensalista', cobranca_id=cobranca.id)
    else:
        form = CobrancaMensalistaStatusForm(initial={'status': cobranca.status})
    return render(request, 'pagamentos/editar_status_cobranca_mensalista.html', {'form': form, 'cobranca': cobranca})

def listar_cobrancas_mensalistas(request):
    cobrancas = CobrancaMensalista.objects.all().order_by('-data_geracao')

    context = {
        'cobrancas': cobrancas,
        'titulo_pagina': 'Listagem de Cobranças Mensalistas'
    }
    return render(request, 'pagamentos/mensalistas/listar_cobrancas_mensalistas.html', context)