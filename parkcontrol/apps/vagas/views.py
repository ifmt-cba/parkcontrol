from datetime import timedelta
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from apps.clientes.models import Mensalista, Diarista
from .models import EntradaVeiculo, SaidaVeiculo, Vaga
from django.utils import timezone
from .forms import EntradaVeiculoForm, SaidaVeiculoForm, SolicitacaoManutencaoForm
from xhtml2pdf import pisa
from django.template.loader import get_template

def registrar_entrada_view(request):
    if request.method == 'POST':
        form = EntradaVeiculoForm(request.POST)
        if form.is_valid():
            entrada = form.save(commit=False)

            # 🔍 Verifica se o cliente existe
            cliente = Mensalista.objects.filter(placa__iexact=entrada.placa).first()
            if not cliente:
                cliente = Diarista.objects.filter(placa__iexact=entrada.placa).first()

            if not cliente:
                messages.error(request, 'Cliente não cadastrado. Cadastre o cliente antes de registrar a entrada.')
                return render(request, 'vagas/entrada.html', {'form': form})
            
            entrada.nome = cliente.nome  # 🆗 Atribui o nome automaticamente

            # 🔐 Verifica se a vaga está livre
            vaga = entrada.vaga
            if vaga.status != 'Livre':
                messages.error(request, f'A vaga {vaga.numero} não está disponível.')
                return render(request, 'vagas/entrada.html', {'form': form})

            # 🚗 Salva entrada e atualiza status da vaga
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
            segundos = tempo.total_seconds()
            mensalista = Mensalista.objects.filter(placa__iexact=placa).first()
            if mensalista:
                valor = 0.0
            elif segundos <= 900:
                valor = 0.0
            else:
                horas = int(segundos // 3600)
                if segundos % 3600 > 0:
                    horas += 1
                valor = horas * 10.0
            tempo_permanencia = str(tempo)
            valor_total = f'{valor:.2f}'
    return JsonResponse({'tempo_permanencia': tempo_permanencia, 'valor_total': valor_total})

def registrar_saida_view(request):
    tempo_permanencia = None
    valor_total = None
    placa = ''
    tipo_cliente = 'Diarista'  # Padrão é diarista
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

                segundos = tempo_permanencia.total_seconds()

                # Verificar se é mensalista
                mensalista = Mensalista.objects.filter(placa__iexact=placa).first()

                if mensalista:
                    tipo_cliente = 'Mensalista'
                    valor_total = 0.0  # Mensalista não paga por hora
                else:
                    tipo_cliente = 'Diarista'
                    # Verificar tolerância de 10 minutos
                    if segundos <= 600:
                        valor_total = 0.0
                    else:
                        horas = int(segundos // 3600)
                        if segundos % 3600 > 0:
                            horas += 1

                        valor_total = horas * 10.0  # Diarista paga 10/hora

                # Criar o registro de saída
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

                # Envia dados do recibo
                return render(request, 'vagas/recibo_saida.html', {
                    'saida': saida,
                    'entrada': entrada,
                    'tipo_cliente': tipo_cliente,
                    'tempo_permanencia': tempo_permanencia,
                    'valor_total': valor_total,
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
            return redirect('vagas:solicitar_manutencao.html')  
    else:
        form = SolicitacaoManutencaoForm()
    return render(request, 'vagas/solicitar_manutencao.html', {'form': form})

def gerar_pdf_recibo(request, saida_id):
    from .models import SaidaVeiculo  # ajuste o caminho se precisar
    saida = SaidaVeiculo.objects.get(id=saida_id)
    entrada = saida.entrada

    template_path = 'vagas/recibo_pdf.html'
    context = {
        'saida': saida,
        'entrada': entrada,
    }

    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="recibo_{saida.placa}.pdf"'

    pisa_status = pisa.CreatePDF(
        html, dest=response
    )

    if pisa_status.err:
        return HttpResponse('Erro na geração do PDF <pre>' + html + '</pre>')
    return response

def relatorio_uso_vagas(request):
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

    return render(request, 'vagas/relatorio.html', context)