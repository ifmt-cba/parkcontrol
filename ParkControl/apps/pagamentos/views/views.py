# apps/pagamentos/views/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from decimal import Decimal
from datetime import datetime, date, timedelta
import calendar
import re 

# Importações de outros apps permanecem como estão (ex: apps.clientes.models)
from apps.clientes.models import Mensalista
from apps.planos.models import Planos

# --- Importações de e-mail ---
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

# --- Modelos e Formulários do app atual ---
from ..models import CobrancaMensalista
from ..forms import GerarCobrancaMensalForm, CobrancaMensalistaStatusForm

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

    valor_devido_calculado = Decimal('0.00')
    if hasattr(cliente_mensalista_obj, 'plano') and cliente_mensalista_obj.plano:
        if isinstance(cliente_mensalista_obj.plano, Planos):
            try:
                plano_do_cliente_obj = Planos.objects.get(
                    id=cliente_mensalista_obj.plano.id,
                    tipo_plano='Mensalista', 
                    status='Ativo' 
                )
                valor_devido_calculado = plano_do_cliente_obj.valor 
            except Planos.DoesNotExist:
                messages.error(request, f"O Plano '{cliente_mensalista_obj.plano.nome}' vinculado ao cliente não é um plano Mensalista ativo. O valor da cobrança será R$0,00.")
        elif isinstance(cliente_mensalista_obj.plano, str):
            plano_nome_from_str = cliente_mensalista_obj.plano
            messages.error(request, f"O cliente '{cliente_mensalista_obj.nome}' está vinculado a um plano com formato inválido ('{plano_nome_from_str}'). Por favor, edite o cliente no Admin e selecione o plano novamente. O valor da cobrança será R$0,00.")
        else:
            messages.error(request, "Cliente possui um plano em formato inesperado. Por favor, verifique o cadastro do cliente. O valor da cobrança será R$0,00.")
    else: 
        messages.error(request, "Cliente não possui um plano definido. Por favor, edite o cliente no Admin e vincule um plano. O valor da cobrança será R$0,00.")
    
    if valor_devido_calculado == Decimal('0.00'):
        messages.warning(request, "Atenção: A cobrança será gerada com valor R$0,00 pois o plano do cliente não foi encontrado ou não é válido. Verifique o plano do cliente no Admin.")

    today = timezone.now().date()
    initial_data = {
        'mes': today.month,
        'ano': today.year,
        # Passa o valor calculado para ser usado no template para exibição
        'valor_devido': valor_devido_calculado 
    }

    if request.method == 'POST':
        # form agora não recebe valor_devido, mas initial_data ainda pode ser passado para manter o mes/ano
        form = GerarCobrancaMensalForm(request.POST, initial=initial_data, request=request) 
        if form.is_valid():
            mes_referencia_str = form.cleaned_data['mes_referencia_str'] 
            data_vencimento = form.cleaned_data['data_vencimento']
            # O valor_devido é o valor_devido_calculado, não vem mais do form.cleaned_data
            valor_final_da_cobranca = valor_devido_calculado

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
                    valor_devido=valor_final_da_cobranca, # Usa o valor calculado
                    status='pendente',
                )
                messages.success(request, f"Cobrança mensal gerada com sucesso para {cliente_mensalista_obj.nome} referente a {mes_referencia_str}.")

            try:
                html_message = render_to_string('pagamentos/enviar_email_cobranca.html', {'cobranca': nova_cobranca})
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

        else: # Formulário inválido (POST)
            # Re-renderiza o form com erros. initial_data já tem valor_devido, mes, ano
            context = {'form': form, 'cliente': cliente_mensalista_obj}
            # A mensagem de warning se valor for 0 já foi adicionada acima.
            return render(request, 'pagamentos/mensalistas/gerar_pagamentos_mensalistas_manual.html', context) 

    else: # Requisição GET (primeira vez que acessa a página)
        # initial_data já está preenchida com mes/ano e valor_devido
        form = GerarCobrancaMensalForm(initial=initial_data, request=request)
        
        context = {'form': form, 'cliente': cliente_mensalista_obj}
        return render(request, 'pagamentos/mensalistas/gerar_pagamentos_mensalistas_manual.html', context)

def gerar_cobranca_imediata(request, cliente_id):
        cliente_mensalista_obj = get_object_or_404(Mensalista, id=cliente_id)

        valor_devido_calculado = Decimal('0.00')
        if hasattr(cliente_mensalista_obj, 'plano') and cliente_mensalista_obj.plano:
            if isinstance(cliente_mensalista_obj.plano, Planos):
                try:
                    plano_do_cliente = Planos.objects.get(
                        nome=cliente_mensalista_obj.plano.nome, 
                        tipo_plano='Mensalista', 
                        status='Ativo' 
                    )
                    valor_devido_calculado = plano_do_cliente.valor 
                except Planos.DoesNotExist:
                    messages.warning(request, f"O Plano '{cliente_mensalista_obj.plano.nome}' não encontrado ou não é um plano Mensalista ativo. Gerando com valor 0.")
                    valor_devido_calculado = Decimal('0.00')
            elif isinstance(cliente_mensalista_obj.plano, str):
                plano_nome_from_str = cliente_mensalista_obj.plano
                try:
                    plano_do_cliente = Planos.objects.get(
                        nome=plano_nome_from_str, 
                        tipo_plano='Mensalista', 
                        status='Ativo' 
                    )
                    valor_devido_calculado = plano_do_cliente.valor 
                    messages.info(request, f"Cliente '{cliente_mensalista_obj.nome}' tinha um plano antigo como string. Cobrança gerada com base em '{plano_nome_from_str}'. Considere atualizar o registro do cliente no Admin.")
                except Planos.DoesNotExist:
                    messages.warning(request, f"Plano '{plano_nome_from_str}' (como texto antigo) não encontrado ou não é um plano Mensalista ativo. Gerando com valor 0.")
                    valor_devido_calculado = Decimal('0.00')
            else:
                messages.warning(request, "Cliente possui um plano em formato inválido. Gerando cobrança com valor 0.")
                valor_devido_calculado = Decimal('0.00')
        else:
            messages.warning(request, "Cliente não possui plano definido ou válido. Gerando cobrança com valor 0.")
            valor_devido_calculado = Decimal('0.00')
            
        today = timezone.now().date()
        mes_referencia_str = today.strftime('%m/%Y')
        data_vencimento = today + timedelta(days=10)
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
                valor_devido=valor_devido_calculado,
                status='pendente',
            )
            messages.success(request, f"Cobrança mensal gerada com sucesso para {cliente_mensalista_obj.nome} referente a {mes_referencia_str}.")
        try:
            html_message = render_to_string('pagamentos/enviar_email_cobranca.html', {'cobranca': nova_cobranca})
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


def cobranca_gerada_confirmacao(request, cobranca_id):
    cobranca = get_object_or_404(CobrancaMensalista, id=cobranca_id)
    return render(request, 'pagamentos/cobranca_gerada_confirmacao.html', {'cobranca': cobranca})

# --- Cobranças de Mensalistas (CRUD para o Contador) ---

def listar_cobrancas_mensalistas(request):
    """
    Lista todas as cobranças de mensalistas, com filtros e paginação.
    Esta view serve como a "Listagem de Pagamentos (Geral)" do caso de uso, focando em mensalistas.
    Os filtros agora incluem nome, plano e estado de pagamento.
    """
    query_nome = request.GET.get('nome_cliente', '').strip()
    query_plano = request.GET.get('plano', '').strip() 
    query_mes = request.GET.get('mes_referencia', '').strip() 
    status_filter = request.GET.get('status', '').strip()

    # Otimização: Garantir que todos os dados relacionados sejam buscados de uma vez
    cobrancas = CobrancaMensalista.objects.select_related(
        'cliente_mensalista__plano' # Já busca o plano
    ).all()

    if query_nome:
        cobrancas = cobrancas.filter(cliente_mensalista__nome__icontains=query_nome)
        
    if query_plano: 
        cobrancas = cobrancas.filter(
            Q(cliente_mensalista__plano__nome__icontains=query_plano)
        )

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

    if not page_obj.object_list and (query_nome or query_plano or query_mes or status_filter != 'todos'):
        messages.info(request, "Nenhuma cobrança de mensalista encontrada com os filtros informados.")

    context = {
        'page_obj': page_obj,
        'query_nome': query_nome,
        'query_plano': query_plano,
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
        html_message = render_to_string('pagamentos/enviar_email_cobranca.html', {'cobranca': cobranca})
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
    if tipo_cobranca_str == 'mensalista':
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