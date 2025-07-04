import logging
from datetime import timedelta
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from apps.pagamentos.models import CobrancaDiaria
from apps.clientes.models import Mensalista, Diarista
from .models import EntradaVeiculo, SaidaVeiculo, SolicitacaoManutencao, Vaga
from django.utils import timezone
from .forms import EntradaVeiculoForm, SaidaVeiculoForm, SolicitacaoManutencaoForm
from django.contrib.auth.decorators import login_required

logger = logging.getLogger('vagas')

@login_required(login_url='login_parkcontrol')
def registrar_entrada_view(request):
    if request.method == 'POST':
        form = EntradaVeiculoForm(request.POST)

        if form.is_valid():
            entrada = form.save(commit=False)

            # 🔍 Verifica se o cliente existe
            cliente = Mensalista.objects.filter(placa__iexact=entrada.placa).first()
            if not cliente:
                cliente = Diarista.objects.filter(placa__iexact=entrada.placa).first()
            logger.info(f"Registro de entrada iniciado para placa {entrada.placa} por {request.user}")
            if not cliente:
                messages.error(request, 'Cliente não cadastrado. Cadastre o cliente antes de registrar a entrada.')
                logger.warning(f"Cliente não encontrado para placa {entrada.placa}")
                return render(request, 'vagas/entrada.html', {'form': form})
            
            entrada.nome = cliente.nome  # 🆗 Atribui o nome automaticamente

             # 🚫 Verifica se já existe uma entrada ativa para essa placa
            entrada_existente = EntradaVeiculo.objects.filter(
                placa__iexact=entrada.placa,
                saidas__isnull=True  # Ajuste para o nome do related_name correto
            ).exists()

            if entrada_existente:
                messages.error(request, 'Entrada já registrada para essa placa.')
                logger.warning(f"Entrada duplicada para placa {entrada.placa}")
                return render(request, 'vagas/entrada.html', {'form': form})

            # 🔐 Verifica se a vaga está livre
            vaga = entrada.vaga
            if vaga.status != 'Livre':
                messages.error(request, f'A vaga {vaga.numero} não está disponível.')
                logger.warning(f"Vaga {vaga.numero} não está livre (status: {vaga.status})")
                return render(request, 'vagas/entrada.html', {'form': form})

            # 🚗 Salva entrada e atualiza status da vaga
            vaga.status = 'Ocupada'
            vaga.save()

            entrada.save()
            messages.success(request, 'Entrada registrada com sucesso!')
            logger.info(f"Entrada registrada: placa={entrada.placa}, vaga={vaga.numero}, por {request.user}")
            return redirect('vagas:registrar_entrada')
    else:
        form = EntradaVeiculoForm()
    return render(request, 'vagas/entrada.html', {'form': form})

@login_required(login_url='login_parkcontrol')
def buscar_nome_por_placa(request):
    placa = request.GET.get('placa')
    nome = ''
    tipo_cliente = ''

    if placa:
        cliente = Mensalista.objects.filter(placa__iexact=placa).first()
        if cliente:
            logger.info(f"Nome buscado por placa: {placa}, tipo: {tipo_cliente}")
            nome = cliente.nome
            tipo_cliente = 'Mensalista'
        else:
            logger.info(f"Nome buscado por placa: {placa}, tipo: {tipo_cliente}")
            cliente = Diarista.objects.filter(placa__iexact=placa).first()
            if cliente:
                nome = cliente.nome
                tipo_cliente = 'Diarista'

    return JsonResponse({'nome': nome, 'tipo_cliente': tipo_cliente})

@login_required(login_url='login_parkcontrol')
def formatar_tempo(tempo):
    horas = tempo.seconds // 3600
    minutos = (tempo.seconds % 3600) // 60
    return f'{horas}h {minutos}min'

@login_required(login_url='login_parkcontrol')
def calcular_valor(placa, tempo):
    segundos = tempo.total_seconds()

    mensalista = Mensalista.objects.filter(placa__iexact=placa).first()
    diarista = Diarista.objects.filter(placa__iexact=placa).first()

    if mensalista:
        return 'Mensalista', 0.0

    if diarista:
        plano = diarista.plano
        valor_plano = plano.valor if plano else 0.0

        if segundos <= 600:
            return 'Diarista', 0.0
        else:
            horas = int(segundos // 3600)
            if segundos % 3600 > 0:
                horas += 1
            valor = horas * float(valor_plano)
            return 'Diarista', valor
    
    # NÃO retorna 'Não cadastrado', só None
    return None, None

@login_required(login_url='login_parkcontrol')
def buscar_saida_por_placa(request):
    placa = request.GET.get('placa')
    tipo_cliente = ''
    tempo_permanencia = ''
    valor_total = ''

    if placa:
        logger.info(f"Consulta de saída iniciada para placa: {placa}")
        entrada = EntradaVeiculo.objects.filter(placa__iexact=placa).order_by('-horario_entrada').first()

        if not entrada:
            return JsonResponse({
                'error': 'Nenhuma entrada encontrada para esta placa.'
            })
        logger.warning(f"Nenhuma entrada encontrada para placa {placa}")
        # Verificar se o cliente é cadastrado
        mensalista = Mensalista.objects.filter(placa__iexact=placa).first()
        diarista = Diarista.objects.filter(placa__iexact=placa).first()

        if not mensalista and not diarista:
            return JsonResponse({
                'error': 'Cliente não cadastrado. Não é possível calcular a saída.'
            })
        logger.warning(f"Cliente com placa {placa} não cadastrado")

        horario_saida = timezone.now()
        tempo = horario_saida - entrada.horario_entrada

        tipo_cliente, valor = calcular_valor(placa, tempo)
        
        tempo_permanencia = formatar_tempo(tempo)
        valor_total = f'{valor:.2f}'
        logger.info(f"Saída simulada: placa={placa}, tipo={tipo_cliente}, tempo={tempo_permanencia}, valor=R${valor_total}")
        return JsonResponse({
            'tipo_cliente': tipo_cliente,
            'tempo_permanencia': tempo_permanencia,
            'valor_total': valor_total
        })

    return JsonResponse({
        'error': 'Placa não informada.'
    })

@login_required(login_url='login_parkcontrol')
def registrar_saida_view(request):
    if request.method == 'POST':
        form = SaidaVeiculoForm(request.POST)
        if form.is_valid():
            placa = form.cleaned_data['placa']
            entrada = EntradaVeiculo.objects.filter(
                placa__iexact=placa
            ).order_by('-horario_entrada').first()
            logger.info(f"Início de registro de saída para placa {placa} por {request.user}")

            if not entrada:
                messages.error(request, '❌ Nenhuma entrada encontrada para esta placa.')
                logger.warning(f"Saída sem entrada para placa {placa}")
                return redirect('vagas:registrar_saida')

            saida_existente = SaidaVeiculo.objects.filter(entrada=entrada).first()
            if saida_existente:
                messages.error(request, '⚠️ Esta entrada já possui uma saída registrada.')
                logger.warning(f"Saída duplicada detectada para entrada de placa {placa}")
                return redirect('vagas:registrar_saida')

            horario_saida = timezone.now()
            tempo_permanencia = horario_saida - entrada.horario_entrada

            tipo_cliente, valor_total = calcular_valor(placa, tempo_permanencia)

            if tipo_cliente == 'Não cadastrado':
                messages.error(request, '❌ Veículo não cadastrado. Cadastre o cliente antes de registrar a saída.')
                logger.warning(f"Veículo com placa {placa} não está cadastrado")
                return redirect('vagas:registrar_saida')

            # Registrar saída
            saida = SaidaVeiculo.objects.create(
                entrada=entrada,
                placa=entrada.placa,
                tempo_permanencia=tempo_permanencia,
                horario_saida=horario_saida,
                valor_total=valor_total,
                tipo_cliente=tipo_cliente,
            )

            # Se for diarista, cria cobrança
            if tipo_cliente == 'Diarista':
                CobrancaDiaria.objects.create(
                    placa=entrada.placa,
                    nome=entrada.nome,
                    data=timezone.now().date(),
                    valor_total=valor_total,
                    status='Pendente',
                    horario_entrada=entrada.horario_entrada,
                    horario_saida=horario_saida
                )

            # Liberar vaga
            entrada.vaga.status = 'Livre'
            entrada.vaga.save()
            entrada.saidas.add(saida)  # Adiciona a saída à entrada

            messages.success(request, '✅ Saída registrada e vaga liberada com sucesso!')
            logger.info(f"Saída registrada: placa={placa}, tempo={tempo_permanencia}, valor=R${valor_total}, por {request.user}")
            if tipo_cliente == 'Diarista':
                messages.success(request, 'Cobrança diária criada com sucesso!')
                logger.info(f"Cobrança diária criada para placa {placa}, valor: R${valor_total}") 
                return redirect('pagamentos:listar_cobranca')
    else:
        form = SaidaVeiculoForm()

    return render(request, 'vagas/saida.html', {'form': form})

@login_required(login_url='login_parkcontrol')
def status_vagas_view(request):
    vagas = Vaga.objects.all().order_by('numero')
    return render(request, 'vagas/status_vagas.html', {'vagas': vagas})

# API para atualizar status em tempo real

@login_required(login_url='login_parkcontrol')
def api_status_vagas(request):
    vagas = Vaga.objects.all().order_by('numero')
    data = []
    for vaga in vagas:
        item = {
            'id': vaga.id,
            'numero': vaga.numero,
            'status': vaga.status,
        }
        if vaga.status == 'Ocupada':
            entrada = EntradaVeiculo.objects.filter(vaga=vaga).order_by('-horario_entrada').first()
            if entrada:
                item['placa'] = entrada.placa
        elif vaga.status == 'Manutenção':
            manutencao = SolicitacaoManutencao.objects.filter(
                numero_vaga=str(vaga.numero),
                resolvido=False
            ).order_by('-data_solicitacao').first()
            if manutencao:
                item['descricao'] = manutencao.descricao
        data.append(item)
        logger.debug("Status das vagas atualizado via API")
    return JsonResponse({'vagas': data})

@login_required(login_url='login_parkcontrol')
def solicitar_manutencao(request):
    if request.method == 'POST':
        form = SolicitacaoManutencaoForm(request.POST)
        if form.is_valid():
            solicitacao = form.save(commit=False)
            solicitacao.solicitante = request.user
            solicitacao.save()

            # Atualizar o status da vaga para "Manutenção"
            vaga = solicitacao.numero_vaga  # Já é um objeto Vaga
            logger.info(f"Usuário {request.user} solicitou manutenção para vaga {vaga.numero}")
            vaga.status = 'Manutenção'
            vaga.save()

            messages.success(request, "Solicitação de manutenção enviada com sucesso!")
            return redirect('vagas:solicitar_manutencao')
    else:
        form = SolicitacaoManutencaoForm()

    return render(request, 'vagas/solicitar_manutencao.html', {'form': form})

@login_required(login_url='login_parkcontrol')
def relatorio_uso_vagas(request):
    logger.info(f"Usuário {request.user} visualizou o relatório de uso de vagas.")
    total_vagas = Vaga.objects.count()
    vagas_ocupadas = Vaga.objects.filter(status='Ocupada').count()
    vagas_livres = total_vagas - vagas_ocupadas

    total_entradas = EntradaVeiculo.objects.count()
    total_saidas = SaidaVeiculo.objects.count()

    # Relatório dos últimos 7 dias
    sete_dias_atras = timezone.now() - timedelta(days=7)
    entradas_7dias = EntradaVeiculo.objects.filter(horario_entrada__gte=sete_dias_atras).count()
    saidas_7dias = SaidaVeiculo.objects.filter(horario_saida__gte=sete_dias_atras).count()

    context = {
        'total_vagas': total_vagas,
        'vagas_ocupadas': vagas_ocupadas,
        'vagas_livres': vagas_livres,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'entradas_7dias': entradas_7dias,
        'saidas_7dias': saidas_7dias,
    }

    return render(request, 'vagas/relatorio_uso.html', context)
