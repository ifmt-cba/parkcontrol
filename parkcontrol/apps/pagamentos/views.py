from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from django.core.paginator import Paginator
from decimal import Decimal

# --- Importações de modelos dos apps ---
from apps.planos.models import Planos
from apps.clientes.models import Mensalista, Diarista
from .models import CobrancaDiarista, CobrancaMensalista
from .forms import GerarCobrancaMensalForm, CobrancaDiaristaStatusForm, CobrancaMensalistaStatusForm


# --- Importações de e-mail ---
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags


# --- Views para Frentista (Cobrança Avulsa) ---

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
    Lista clientes Mensalista
    """
    query_nome = request.GET.get('nome_cliente', '').strip()
    status_filter = request.GET.get('status', 'ativo').strip()
    query_placa = request.GET.get('placa_veiculo', '').strip()

    clientes_base_query = Mensalista.objects.all().order_by('nome') 

    clientes_filtrados = clientes_base_query
    if status_filter == 'ativo':
        clientes_filtrados = clientes_filtrados.filter(ativo=True)
    elif status_filter == 'inativo':
        clientes_filtrados = clientes_filtrados.filter(ativo=False)
    
    if query_nome:
        clientes_filtrados = clientes_filtrados.filter(nome__icontains=query_nome) 

    if query_placa:
        clientes_filtrados = clientes_filtrados.filter(placa__icontains=query_placa)
    
    clientes_com_cobrancas = []
    for cliente in clientes_filtrados: 
        ultima_cobranca = CobrancaMensalista.objects.filter(
            cliente_mensalista=cliente
        ).order_by('-data_geracao').first() 

        cobranca_pendente_para_email = CobrancaMensalista.objects.filter(
            cliente_mensalista=cliente, 
            status__in=['pendente', 'parcialmente_pago']
        ).order_by('data_vencimento').first() 

        cliente_dict = {
            'obj': cliente, 
            'ultima_cobranca': ultima_cobranca,
            'cobranca_pendente_para_email': cobranca_pendente_para_email, 
        }
        clientes_com_cobrancas.append(cliente_dict)

    paginator = Paginator(clientes_com_cobrancas, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pagamentos/mensalistas/gerar_pagamentos_mensalistas_lista_clientes.html', {
        'titulo_pagina': 'Gerar Cobrança: Clientes Mensalistas',
        'page_obj': page_obj, 
        'query_nome': query_nome,
        'status_filter': status_filter,
        'query_placa': query_placa,
        'status_choices': [('ativo', 'Ativo'), ('inativo', 'Inativo'), ('todos', 'Todos')]
    })

def gerar_pagamentos_mensalistas_manual(request, cliente_id): 
    cliente_mensalista_obj = get_object_or_404(Mensalista, id=cliente_id) 

    initial_data = {}
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
            mes_referencia_str = form.cleaned_data['mes_referencia']
            data_vencimento = form.cleaned_data['data_vencimento']
            valor_devido = form.cleaned_data['valor_devido']

            if CobrancaMensalista.objects.filter(
                cliente_mensalista=cliente_mensalista_obj, 
                mes_referencia=mes_referencia_str,
            ).exists():
                messages.error(request, f"Já existe uma cobrança mensal para {cliente_mensalista_obj.nome} referente ao mês {mes_referencia_str}. Não será gerada novamente.")
                return redirect('pagamentos:gerar_pagamentos_mensalistas_lista_clientes') 

            with transaction.atomic():
                nova_cobranca = CobrancaMensalista.objects.create( 
                    cliente_mensalista=cliente_mensalista_obj, 
                    mes_referencia=mes_referencia_str,
                    data_vencimento=data_vencimento,
                    valor_devido=valor_devido,
                    status='pendente',
                )
                messages.success(request, f"Cobrança mensal gerada com sucesso para {cliente_mensalista_obj.nome} referente a {mes_referencia_str}.")

            try:
                html_message = render_to_string('pagamentos/email_cobranca_template.html', {'cobranca': nova_cobranca})
                plain_message = strip_tags(html_message)
                send_mail(
                    subject=f"ParkControl: Nova Cobrança Gerada #{nova_cobranca.id}",
                    message=plain_message, from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[cliente_mensalista_obj.email], 
                    html_message=html_message, fail_silently=False,
                )
                messages.info(request, f"E-mail de cobrança enviado para {cliente_mensalista_obj.email}.")
            except Exception as e:
                messages.error(request, f"Erro ao enviar e-mail após geração: {e}. Verifique as configurações de e-mail.")

            return redirect('pagamentos:cobranca_gerada_confirmacao', cobranca_id=nova_cobranca.id) 

        else:
            return render(request, 'pagamentos/mensalistas/gerar_pagamentos_mensalistas_manual.html', {'form': form, 'cliente': cliente_mensalista_obj}) 

    else: 
        form = GerarCobrancaMensalForm(initial=initial_data, request=request)

    context = {'form': form, 'cliente': cliente_mensalista_obj} 
    return render(request, 'pagamentos/mensalistas/gerar_pagamentos_mensalistas_manual.html', context)

def gerar_pagamentos_diaristas_lista_clientes(request):
    """
    Lista clientes Diaristas para que o contador possa gerenciar movimentos e cobranças para eles.
    """
    query_nome = request.GET.get('nome_cliente', '').strip()
    query_placa = request.GET.get('placa_veiculo', '').strip()
    status_filter = request.GET.get('status', 'ativo').strip()

    # Consulta Diarista do app clientes
    clientes_base_query = Diarista.objects.all().order_by('nome') 

    clientes_filtrados = clientes_base_query
    if status_filter == 'ativo':
        clientes_filtrados = clientes_filtrados.filter(ativo=True)
    elif status_filter == 'inativo':
        clientes_filtrados = clientes_filtrados.filter(ativo=False)
    
    if query_nome:
        clientes_filtrados = clientes_filtrados.filter(nome__icontains=query_nome) 

    if query_placa:
        clientes_filtrados = clientes_filtrados.filter(placa__icontains=query_placa)
    diaristas_com_info = []
    for diarista in clientes_filtrados:
        
        diarista_dict = {
            'obj': diarista,
        }
        diaristas_com_info.append(diarista_dict)

    paginator = Paginator(diaristas_com_info, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if not page_obj.object_list and (query_nome or query_placa or status_filter != 'todos'): 
        messages.info(request, "Nenhum cliente diarista encontrado com os filtros informados.")

    return render(request, 'pagamentos/diaristas/gerar_pagamentos_diaristas_lista_clientes.html', {
        'titulo_pagina': 'Gerar Cobrança: Clientes Diaristas',
        'page_obj': page_obj, 
        'query_nome': query_nome,
        'status_filter': status_filter,
        'query_placa': query_placa,
        'status_choices': [('ativo', 'Ativo'), ('inativo', 'Inativo'), ('todos', 'Todos')]
    })

def cobranca_gerada_confirmacao(request, cobranca_id):
    cobranca = get_object_or_404(CobrancaMensalista, id=cobranca_id)

    try:
         html_message = render_to_string('pagamentos/email_cobranca_template.html', {'cobranca': cobranca})
         plain_message = strip_tags(html_message)
         send_mail(
             subject=f"ParkControl: Nova Cobrança Gerada #{cobranca.id}",
             message=plain_message, from_email=settings.DEFAULT_FROM_EMAIL,
             recipient_list=[cobranca.cliente_mensalista.email], html_message=html_message, fail_silently=False,
         )
         messages.info(request, f"E-mail de cobrança enviado para {cobranca.cliente_mensalista.email}.")
    except Exception as e:
         messages.error(request, f"Erro ao enviar e-mail após geração: {e}.")
    
    return render(request, 'pagamentos/cobranca_gerada_confirmacao.html', {'cobranca': cobranca})


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
    return render(request, 'pagamentos/mensalistas/listar_cobrancas.html', context)

def detalhe_cobranca_mensalista(request, cobranca_id):
    cobranca = get_object_or_404(CobrancaMensalista, id=cobranca_id)
    return render(request, 'pagamentos/mensalistas/detalhe_cobranca_mensalista.html', {'cobranca': cobranca})

def editar_cobranca_mensalista_status(request, cobranca_id):
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
        html_message = render_to_string('pagamentos/email_cobranca_template.html', {'cobranca': cobranca})
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
        'nome_estacionamento': 'ParkControl Estacionamento',
    }
    return render(request, 'pagamentos/recibo.html', context)