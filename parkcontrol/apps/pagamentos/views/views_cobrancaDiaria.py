from django.shortcuts import render, redirect, get_object_or_404
from apps.vagas.models import SaidaVeiculo
from ..models import CobrancaDiaria

def formatar_tempo(tempo):
    total_seconds = int(tempo.total_seconds())
    horas = total_seconds // 3600
    minutos = (total_seconds % 3600) // 60
    segundos = total_seconds % 60
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

def listar_cobrancas(request):
    cobrancas = CobrancaDiaria.objects.all().order_by('-data')
    return render(request, 'pagamentos/listar_cobranca.html', {'cobrancas': cobrancas})

def atualizar_status_cobranca(request, cobranca_id):
    cobranca = get_object_or_404(CobrancaDiaria, id=cobranca_id)
    cobranca.status = 'Pago'
    cobranca.save()
    return redirect('pagamentos:listar_cobranca')

def emitir_recibo(request, cobranca_id):
    cobranca = get_object_or_404(CobrancaDiaria, id=cobranca_id)

    # Buscar a entrada correspondente pela placa e horário_entrada da cobrança
    entrada = None
    saida = None
    from apps.vagas.models import EntradaVeiculo
    entrada = EntradaVeiculo.objects.filter(
        placa__iexact=cobranca.placa,
        horario_entrada=cobranca.horario_entrada
    ).first()

    if entrada:
        saida = SaidaVeiculo.objects.filter(entrada=entrada).first()

    if saida and saida.tempo_permanencia:
        tempo_formatado = formatar_tempo(saida.tempo_permanencia)
    else:
        tempo_formatado = "00:00:00"
    context = {
        'cobranca': cobranca,
        'entrada': entrada,
        'saida': saida,
        'tempo_permanencia_formatado': tempo_formatado,
    }

    return render(request, 'pagamentos/emitir_recibo.html', context)
