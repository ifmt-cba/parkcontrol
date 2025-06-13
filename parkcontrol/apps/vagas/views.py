from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from apps.clientes.models import Mensalista, Diarista
from .models import EntradaVeiculo, SaidaVeiculo, Vaga
from django.utils import timezone
from .forms import EntradaVeiculoForm, SaidaVeiculoForm, SolicitacaoManutencaoForm

def registrar_entrada_view(request):
    if request.method == 'POST':
        form = EntradaVeiculoForm(request.POST)
        if form.is_valid():
            entrada = form.save(commit=False)

            # Atualiza o status da vaga para "Ocupada"
            vaga = entrada.vaga
            if vaga.status != 'Livre':
                messages.error(request, f'A vaga {vaga.numero} não está disponível.')
                return render(request, 'vagas/entrada.html', {'form': form})
            
            vaga.status = 'Ocupada'
            vaga.save()

            entrada.save()
            messages.success(request, 'Entrada registrada com sucesso!')
            return redirect('vagas:registrar_entrada')
    else:
        form = EntradaVeiculoForm()
    return render(request, 'vagas/entrada.html', {'form': form})

def buscar_nome_por_placa(request):
    placa = request.GET.get('placa')
    nome = ''
    if placa:
        cliente = Mensalista.objects.filter(placa__iexact=placa).first()
        if not cliente:
            cliente = Diarista.objects.filter(placa__iexact=placa).first()
        if cliente:
            nome = cliente.nome
    return JsonResponse({'nome': nome})

def buscar_saida_por_placa(request):
    placa = request.GET.get('placa')
    tempo_permanencia = ''
    valor_total = ''
    if placa:
        entrada = EntradaVeiculo.objects.filter(placa__iexact=placa).order_by('-horario_entrada').first()
        if entrada:
            horario_saida = timezone.now()
            tempo = horario_saida - entrada.horario_entrada
            horas = int(tempo.total_seconds() // 3600)
            if tempo.total_seconds() % 3600 > 0:
                horas += 1
            valor = horas * 10.0
            tempo_permanencia = str(tempo)
            valor_total = f'{valor:.2f}'
    return JsonResponse({'tempo_permanencia': tempo_permanencia, 'valor_total': valor_total})

def registrar_saida_view(request):
    tempo_permanencia = None
    valor_total = None
    placa = ''
    if request.method == 'POST':
        form = SaidaVeiculoForm(request.POST)
        if form.is_valid():
            placa = form.cleaned_data['placa']
            entrada = EntradaVeiculo.objects.filter(placa__iexact=placa).order_by('-horario_entrada').first()
            if not entrada:
                messages.error(request, 'Nenhuma entrada encontrada para esta placa.')
            else:
                horario_saida = timezone.now()
                tempo_permanencia = horario_saida - entrada.horario_entrada
                horas = int(tempo_permanencia.total_seconds() // 3600)
                if tempo_permanencia.total_seconds() % 3600 > 0:
                    horas += 1
                valor_total = horas * 10.0

                # Cria o registro de saída
                saida = SaidaVeiculo.objects.create(
                    entrada=entrada,
                    placa=placa,
                    tempo_permanencia=tempo_permanencia,
                    horario_saida=horario_saida,
                    valor_total=valor_total
                )

                # Libera a vaga
                entrada.vaga.status = 'Livre'
                entrada.vaga.save()

                messages.success(request, 'Saída registrada com sucesso!')
                return render(request, 'vagas/saida.html', {
                    'form': SaidaVeiculoForm(),
                    'saida': saida,
                    'sucesso': True
                })
    else:
        form = SaidaVeiculoForm()
    return render(request, 'vagas/saida.html', {
        'form': form,
        'saida': None,
        'sucesso': False
    })

def listar_vagas(request):
    vagas = Vaga.objects.all()
    return render(request, 'vagas/listar_vagas.html', {'vagas': vagas})

def solicitar_manutencao(request):
    if request.method == 'POST':
        form = SolicitacaoManutencaoForm(request.POST)
        if form.is_valid():
            solicitacao = form.save(commit=False)
            solicitacao.solicitante = request.user
            solicitacao.save()
            return redirect('vagas/solicitar_manutencao.html')  
    else:
        form = SolicitacaoManutencaoForm()
    return render(request, 'vagas/solicitar_manutencao.html', {'form': form})