# apps/pagamentos/views.py

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

# --- Importações de modelos dos apps ---
from apps.usuarios.models import Usuario 
from apps.clientes.models import Mensalista
from apps.planos.models import Planos

# --- Importações de e-mail ---
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

# --- Modelos app pagamentos ---
from .models import Movimento, ConfiguracaoTarifa, CobrancaDiarista, CobrancaMensalista
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

def listagem_pagamentos_geral_redirect(request):
    """
    View auxiliar para o botão "Visualizar e Editar Pagamentos"
    """
    return redirect('pagamentos:listar_cobrancas_mensalistas') 

def gerar_pagamentos_mensalistas_lista_clientes(request):
    """
    Lista clientes Mensalista para que o contador possa gerar cobranças para eles.
    """
    query_nome = request.GET.get('nome_cliente', '').strip()
    status_filter = request.GET.get('status', 'ativo').strip()
    query_placa = request.GET.get('placa_veiculo', '').strip()

    clientes = Mensalista.objects.all().order_by('nome')

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

    if query_nome:
        clientes = clientes.filter(nome__icontains=query_nome)

    if query_placa:
        clientes = clientes.filter(placa__icontains=query_placa)

    paginator = Paginator(clientes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if not page_obj.object_list and (query_nome or query_placa or status_filter != 'todos'): 
        messages.info(request, "Nenhum cliente mensalista encontrado com os filtros informados.")

    return render(request, 'pagamentos/mensalistas/gerar_pagamentos_mensalistas_lista_clientes.html', {
        'titulo_pagina': 'Clientes Mensalistas',
        'page_obj': page_obj,
        'query_nome': query_nome,
        'status_filter': status_filter,
        'query_placa': query_placa,
        'status_choices': [('ativo', 'Ativo'), ('inativo', 'Inativo'), ('todos', 'Todos')]
    })

def gerar_pagamentos_mensalistas_manual(request, cliente_id=None): 
    """
    Gerar Pagamentos Mensalistas.
    """
    initial_data = {}
    cliente_mensalista_obj = None

    if cliente_id:
        cliente_mensalista_obj = get_object_or_404(Mensalista, id=cliente_id)
        initial_data['cliente_mensalista'] = cliente_mensalista_obj.id
        
        if hasattr(cliente_mensalista_obj, 'plano') and cliente_mensalista_obj.plano:
            try:
                plano_do_cliente = Planos.objects.get(
                    nome=cliente_mensalista_obj.plano, 
                    tipo_plano='Mensalista', 
                    status='Ativo' 
                )
                initial_data['valor_devido'] = plano_do_cliente.valor 
            except Planos.DoesNotExist:
                messages.warning(request, f"Plano '{cliente_mensalista_obj.plano}' não encontrado ou não é um plano Mensalista. Preencha o valor manualmente.")
                initial_data['valor_devido'] = Decimal('0.00') 
        else:
            messages.warning(request, "Cliente não possui plano definido ou válido. Preencha o valor manualmente.")

        today = timezone.now().date()
        initial_data['mes_referencia'] = today.strftime('%m/%Y')

    if request.method == 'POST':
        form = GerarCobrancaMensalForm(request.POST, request=request) 
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
        form = GerarCobrancaMensalForm(initial=initial_data, request=request)

    context = {'form': form}
    return render(request, 'pagamentos/mensalistas/gerar_pagamentos_mensalistas_manual.html', context)

def listar_cobrancas_diaristas(request):
    """
    Lista todas as cobranças de diaristas, com filtros e paginação.
    """
    query_placa = request.GET.get('placa_veiculo', '').strip()
    status_filter = request.GET.get('status', '').strip()

    cobrancas = CobrancaDiarista.objects.select_related('movimento').all()

    if query_placa:
        cobrancas = cobrancas.filter(movimento__placa_veiculo__icontains=query_placa)
    if status_filter:
        cobrancas = cobrancas.filter(status=status_filter)
    
    cobrancas = cobrancas.order_by('-data_geracao')

    paginator = Paginator(cobrancas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if not page_obj.object_list and (query_placa or status_filter != 'todos'):
        messages.info(request, "Nenhuma cobrança de diarista encontrada com os filtros informados.")

    context = {
        'page_obj': page_obj,
        'query_placa': query_placa,
        'status_filter': status_filter,
        'status_choices': CobrancaDiarista.STATUS_CHOICES + [('todos', 'Todos')],
    }
    return render(request, 'pagamentos/diaristas/listar_cobrancas_diaristas.html', context)

def detalhe_cobranca_diarista(request, cobranca_id):
    """
    Exibe os detalhes de uma cobrança de diarista específica.
    """
    cobranca = get_object_or_404(CobrancaDiarista, id=cobranca_id)
    return render(request, 'pagamentos/diaristas/detalhe_cobranca_diarista.html', {'cobranca': cobranca})

def editar_cobranca_diarista_status(request, cobranca_id):
    """
    Permite ao contador editar o status e valor pago de uma cobrança de diarista.
    """
    cobranca = get_object_or_404(CobrancaDiarista, id=cobranca_id)
    
    if request.method == 'POST':
        form = CobrancaDiaristaStatusForm(request.POST, instance=cobranca) 
        if form.is_valid():
            with transaction.atomic():
                form.save()
                messages.success(request, f"Status da cobrança de diarista {cobranca.id} atualizado para '{cobranca.get_status_display()}'.")
                if cobranca.status == 'pago' and not cobranca.data_pagamento:
                    cobranca.data_pagamento = timezone.now()
                    cobranca.save()
                return redirect('pagamentos:detalhe_cobranca_diarista', cobranca_id=cobranca.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    field_name = form[field].label or field
                    messages.error(request, f"Erro no campo '{field_name}': {error}")
    else:
        form = CobrancaDiaristaStatusForm(instance=cobranca)
    
    return render(request, 'pagamentos/diaristas/editar_cobranca_diarista_status.html', {'form': form, 'cobranca': cobranca})

def excluir_cobranca_diarista(request, cobranca_id):
    """
    Confirma e executa a exclusão de uma cobrança de diarista.
    """
    cobranca = get_object_or_404(CobrancaDiarista, id=cobranca_id)
    if request.method == 'POST':
        cobranca.delete()
        messages.success(request, f"Cobrança de diarista {cobranca_id} excluída com sucesso.")
        return redirect('pagamentos:listar_cobrancas_diaristas')
    return render(request, 'pagamentos/diaristas/excluir_cobranca_diarista_confirm.html', {'cobranca': cobranca})

# --- Cobranças de Mensalistas (CRUD para o Contador) ---

def listar_cobrancas_mensalistas(request):
    """
    Lista todas as cobranças de mensalistas, com filtros e paginação.
    Esta view serve como a "Listagem de Pagamentos (Geral)" do caso de uso, focando em mensalistas.
    """
    query_nome = request.GET.get('nome_cliente', '').strip()
    query_mes = request.GET.get('mes_referencia', '').strip()
    status_filter = request.GET.get('status', '').strip()

    cobrancas = CobrancaMensalista.objects.select_related('cliente_mensalista__nome', 'cliente_mensalista__plano').all()

    if query_nome:
        cobrancas = cobrancas.filter(cliente_mensalista__nome__icontains=query_nome)
    if query_mes:
        if re.match(r'^(0[1-9]|1[0-2])/\d{4}$', query_mes):
            cobrancas = cobrancas.filter(mes_referencia=query_mes)
        else:
            messages.error(request, "Formato de Mês/Ano inválido para filtro. Use MM/AAAA.")
    if status_filter:
        cobrancas = cobrancas.filter(status=status_filter)
    
    cobrancas = cobrancas.order_by('-data_vencimento', '-data_geracao')

    paginator = Paginator(cobrancas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if not page_obj.object_list and (query_nome or query_mes or status_filter != 'todos'):
        messages.info(request, "Nenhuma cobrança de mensalista encontrada com os filtros informados.")

    context = {
        'page_obj': page_obj,
        'query_nome': query_nome,
        'query_mes': query_mes,
        'status_filter': status_filter,
        'status_choices': CobrancaMensalista.STATUS_CHOICES + [('todos', 'Todos')],
    }
    return render(request, 'pagamentos/mensalistas/listar_cobrancas_mensalistas.html', context)

def detalhe_cobranca_mensalista(request, cobranca_id):
    """
    Exibe os detalhes de uma cobrança de mensalista específica.
    """
    cobranca = get_object_or_404(CobrancaMensalista, id=cobranca_id)
    return render(request, 'pagamentos/mensalistas/detalhe_cobranca_mensalista.html', {'cobranca': cobranca})

def editar_cobranca_mensalista_status(request, cobranca_id):
    """
    Permite ao contador editar o status e valor pago de uma cobrança de mensalista.
    """
    cobranca = get_object_or_404(CobrancaMensalista, id=cobranca_id)
    
    if request.method == 'POST':
        form = CobrancaMensalistaStatusForm(request.POST, instance=cobranca) 
        if form.is_valid():
            with transaction.atomic():
                form.save()
                messages.success(request, f"Status da cobrança de mensalista {cobranca.id} atualizado para '{cobranca.get_status_display()}'.")
                if cobranca.status == 'pago' and not cobranca.data_pagamento:
                    cobranca.data_pagamento = timezone.now()
                    cobranca.save()
                return redirect('pagamentos:detalhe_cobranca_mensalista', cobranca_id=cobranca.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    field_name = form[field].label or field
                    messages.error(request, f"Erro no campo '{field_name}': {error}")
    else:
        form = CobrancaMensalistaStatusForm(instance=cobranca)
    
    return render(request, 'pagamentos/mensalistas/editar_cobranca_mensalista_status.html', {'form': form, 'cobranca': cobranca})

def excluir_cobranca_mensalista(request, cobranca_id):
    """
    Confirma e executa a exclusão de uma cobrança de mensalista.
    """
    cobranca = get_object_or_404(CobrancaMensalista, id=cobranca_id)
    if request.method == 'POST':
        cobranca.delete()
        messages.success(request, f"Cobrança de mensalista {cobranca_id} excluída com sucesso.")
        return redirect('pagamentos:listar_cobrancas_mensalistas')
    return render(request, 'pagamentos/mensalistas/excluir_cobranca_mensalista_confirm.html', {'cobranca': cobranca})

def listar_cobrancas_para_email(request):
    """
    Lista as cobranças de mensalistas que estão "Em aberto" (pendentes ou parcialmente pagas)
    para o contador poder enviar e-mail de cobrança.
    RN01 - Somente pagamentos com status "Pendente" ou "Parcialmente Pago" (em aberto) devem ser exibidos.
    """
    query_nome = request.GET.get('nome_cliente', '').strip()
    
    cobrancas_em_aberto = CobrancaMensalista.objects.filter(
        Q(status='pendente') | Q(status='parcialmente_pago')
    ).select_related('cliente_mensalista').all()

    if query_nome:
        cobrancas_em_aberto = cobrancas_em_aberto.filter(
            cliente_mensalista__nome__icontains=query_nome
        )
    
    paginator = Paginator(cobrancas_em_aberto, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if not page_obj.object_list and query_nome:
        messages.info(request, "Nenhum resultado para os filtros informados.")

    context = {
        'page_obj': page_obj, 
        'query_nome': query_nome,
    }
    return render(request, 'pagamentos/mensalistas/enviar_email_cobranca.html', context)

def disparar_email_cobranca(request, cobranca_id):
    """
    Lógica para realmente enviar o e-mail de cobrança para uma cobrança específica de mensalista.
    """
    cobranca = get_object_or_404(CobrancaMensalista, id=cobranca_id)

    if not (cobranca.status == 'pendente' or cobranca.status == 'parcialmente_pago'):
        messages.error(request, "Não é possível enviar e-mail para cobranças já pagas ou canceladas.")
        return redirect('pagamentos:listar_cobrancas_para_email')

    if not cobranca.cliente_mensalista or not cobranca.cliente_mensalista.email: 
        messages.error(request, "Cliente mensalista não associado ou e-mail de cobrança não disponível para esta cobrança.")
        return redirect('pagamentos:listar_cobrancas_para_email')

    try:
        html_message = render_to_string('pagamentos/email/email_cobranca_template.html', {'cobranca': cobranca})
        plain_message = strip_tags(html_message)

        send_mail(
            subject=f"ParkControl: Lembrete de Cobrança #{cobranca.id} - Ref. {cobranca.mes_referencia}",
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[cobranca.cliente_mensalista.email],
            html_message=html_message,
            fail_silently=False,
        )
        messages.success(request, f"E-mail de cobrança enviado com sucesso para {cobranca.cliente_mensalista.email}.")
    except Exception as e:
        messages.error(request, f"Erro ao enviar e-mail: {e}. Verifique as configurações de e-mail.")
    
    return redirect('pagamentos:listar_cobrancas_para_email')

def emitir_recibo(request, cobranca_id, tipo_cobranca_str):
    """
    View para emitir recibo de uma cobrança, seja diarista ou mensalista.
    tipo_cobranca_str deve ser 'diarista' ou 'mensalista'.
    """
    if tipo_cobranca_str == 'diarista':
        cobranca = get_object_or_404(CobrancaDiarista, id=cobranca_id)
    elif tipo_cobranca_str == 'mensalista':
        cobranca = get_object_or_404(CobrancaMensalista, id=cobranca_id)
    else:
        messages.error(request, "Tipo de cobrança inválido para emitir recibo.")
        return redirect('home_parkcontrol')

    if not cobranca.esta_paga() and cobranca.status != 'parcialmente_pago':
        messages.warning(request, "Não é possível emitir recibo para uma cobrança não paga ou parcialmente paga (sem valor pago).")
        if tipo_cobranca_str == 'diarista':
            return redirect('pagamentos:detalhe_cobranca_diarista', cobranca_id=cobranca.id)
        else:
            return redirect('pagamentos:detalhe_cobranca_mensalista', cobranca_id=cobranca.id)

    context = {
        'cobranca': cobranca, 'data_emissao': timezone.now(), 'tipo_cobranca': tipo_cobranca_str,
        'nome_estacionamento': 'ParkControl Estacionamento', 'endereco_estacionamento': 'Rua Exemplo, 123 - Cidade - UF',
        'cnpj_estacionamento': 'XX.XXX.XXX/YYYY-ZZ',
    }
    return render(request, 'pagamentos/recibo.html', context)