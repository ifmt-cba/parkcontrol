from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from decimal import Decimal
from datetime import datetime, date
import calendar
import re 
from django.core.paginator import Paginator

from apps.usuarios.models import Usuario 
from apps.clientes.models import Mensalista
from apps.planos.models import Planos

# Importações de e-mail
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

from .models import Movimento, ConfiguracaoTarifa, PlanoMensal, CobrancaDiarista, CobrancaMensalista
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

# --- Views para Contador (Gerenciamento de Pagamentos) ---


def gerenciamento_pagamentos_home(request):
    """
    Interface principal do módulo Gerenciamento de Pagamentos para o Contador.
    """
    return render(request, 'pagamentos/gerenciamento_pagamentos_home.html')

def gerar_pagamentos_mensalistas_lista_clientes(request):
    """
    Lista clientes Mensalista (do app clientes) para que o contador possa gerar cobranças para eles.
    """
    query_nome = request.GET.get('nome_cliente', '').strip()
    status_filter = request.GET.get('status', 'ativo').strip() # Default para 'ativo'
    query_placa = request.GET.get('placa_veiculo', '').strip()

    # --- CONSULTA AGORA USA Mensalista do app clientes ---
    clientes = Mensalista.objects.all().order_by('nome') # Ordena por nome do Mensalista

    print(f"\n--- DEBUG View gerar_pagamentos_mensalistas_lista_clientes ---")
    print(f"URL Params: {request.GET}")
    print(f"Query Nome (do filtro): '{query_nome}'")
    print(f"Query Placa (do filtro): '{query_placa}'")
    print(f"Status Filter (do filtro): '{status_filter}'")
    print(f"Total Mensalista ANTES dos filtros (na view, após order_by): {clientes.count()}")

    if status_filter == 'ativo':
        clientes = clientes.filter(ativo=True)
    elif status_filter == 'inativo':
        clientes = clientes.filter(ativo=False)
    
    print(f"Total Mensalista APÓS filtro de Status: {clientes.count()}")

    if query_nome:
        clientes = clientes.filter(nome__icontains=query_nome) # Filtra pelo campo 'nome' do Mensalista
    
    print(f"Total Mensalista APÓS filtro de Nome: {clientes.count()}")

    if query_placa:
        # Mensalista (do app clientes) tem um campo 'placa', então o filtro é direto.
        clientes = clientes.filter(placa__icontains=query_placa)
        print(f"Total Mensalista APÓS filtro de Placa: {clientes.count()}")
    
    print(f"Consulta SQL final: {clientes.query}")
    print(f"Clientes no QuerySet final (objetos): {list(clientes)}") 
    print(f"--- Fim DEBUG View gerar_pagamentos_mensalistas_lista_clientes ---\n")

    paginator = Paginator(clientes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if not page_obj.object_list and (query_nome or query_placa or status_filter != 'todos'): 
        messages.info(request, "Nenhum cliente mensalista encontrado com os filtros informados.")

    return render(request, 'pagamentos/mensalistas/gerar_pagamentos_mensalistas_lista_clientes.html', {
        'titulo_pagina': 'Gerar Cobrança: Clientes Mensalistas',
        'page_obj': page_obj,
        'query_nome': query_nome,
        'status_filter': status_filter,
        'query_placa': query_placa,
        'status_choices': [('ativo', 'Ativo'), ('inativo', 'Inativo'), ('todos', 'Todos')]
    })

def listagem_pagamentos_geral_redirect(request):
    """
    View auxiliar para o botão "Visualizar e Editar Pagamentos"
    """
    return redirect('pagamentos:listar_cobrancas_mensalistas') 

def gerar_pagamentos_mensalistas_manual(request, cliente_id=None): 
    """
    Gerar Pagamentos Mensalistas (manual pelo contador).
    Pode receber um cliente_id (do modelo Mensalista) para pré-preencher o formulário.
    """
    initial_data = {}
    cliente_mensalista_obj = None

    if cliente_id:
        cliente_mensalista_obj = get_object_or_404(Mensalista, id=cliente_id)
        initial_data['cliente_mensalista'] = cliente_mensalista_obj.id
        
        if hasattr(cliente_mensalista_obj, 'plano') and cliente_mensalista_obj.plano:
            try:
                plano_do_cliente = Planos.objects.get(nome=cliente_mensalista_obj.plano, tipo_plano='Mensalista')
                initial_data['valor_devido'] = plano_do_cliente.valor
            except Planos.DoesNotExist:
                messages.warning(request, f"Plano '{cliente_mensalista_obj.plano}' não encontrado ou não é um plano Mensalista. Preencha o valor manualmente.")
                initial_data['valor_devido'] = Decimal('0.00')

        today = timezone.now().date()
        initial_data['mes_referencia'] = today.strftime('%m/%Y')

    if request.method == 'POST':
        form = GerarCobrancaMensalForm(request.POST)
        if form.is_valid():

            cliente_mensalista_id = form.cleaned_data['cliente_mensalista'] 
            cliente_mensalista_obj_from_form = get_object_or_404(Mensalista, id=cliente_mensalista_id)

            mes_referencia_str = form.cleaned_data['mes_referencia']
            data_vencimento = form.cleaned_data['data_vencimento']
            valor_devido = form.cleaned_data['valor_devido']

            with transaction.atomic():
                CobrancaMensalista.objects.create(
                    cliente_mensalista=cliente_mensalista_obj_from_form,
                    mes_referencia=mes_referencia_str,
                    data_vencimento=data_vencimento,
                    valor_devido=valor_devido,
                    status='pendente',
                )
                messages.success(request, f"Cobrança mensal gerada com sucesso para {cliente_mensalista_obj_from_form.nome} referente a {mes_referencia_str}.")
            return redirect('pagamentos:listar_cobrancas_mensalistas')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    field_name = form[field].label or field
                    messages.error(request, f"Erro no campo '{field_name}': {error}")
            return render(request, 'pagamentos/mensalistas/gerar_pagamentos_mensalistas_manual.html', {'form': form})
    else:
        form = GerarCobrancaMensalForm(initial=initial_data)

    context = {'form': form}
    return render(request, 'pagamentos/mensalistas/gerar_pagamentos_mensalistas_manual.html', context)

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