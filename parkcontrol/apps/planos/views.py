import logging
from django.shortcuts import render, get_object_or_404, redirect
from .models import Planos
from .forms import PlanoMensalForm, PlanoDiarioForm
from django.contrib.auth.decorators import login_required

logger = logging.getLogger('planos')

@login_required(login_url='login_parkcontrol')
def selecao_plano(request):
    logger.info(f"Usuário {request.user} acessou a seleção de planos.")
    return render(request, 'tela_principal/selecao_plano.html')

@login_required(login_url='login_parkcontrol')
def listar_planos_diarios(request):
    logger.info(f"Usuário {request.user} listou os planos diaristas.")
    planos = Planos.objects.filter(tipo_plano='Diarista')
    return render(request, 'planos/diarios/listar_planos_diarios.html', {'planos': planos})

@login_required(login_url='login_parkcontrol')
def listar_planos_mensais(request):
    logger.info(f"Usuário {request.user} listou os planos mensalistas.")
    planos = Planos.objects.filter(tipo_plano='Mensalista')
    return render(request, 'planos/mensais/listar_planos_mensais.html', {'planos': planos})

@login_required(login_url='login_parkcontrol')
def criar_plano_mensal(request):
    if request.method == 'POST':
        form = PlanoMensalForm(request.POST)
        if form.is_valid():
            plano = form.save(commit=False)
            plano.tipo_plano = 'Mensalista'
            tipo_mensal = form.cleaned_data.get('tipo_mensal')
            if not tipo_mensal:
                form.add_error('tipo_mensal', 'O campo Tipo Mensal é obrigatório.')
                return render(request, 'planos/mensais/criar_plano_mensal.html', {'form': form})
            plano.tipo_mensal = tipo_mensal
            plano.save()
            logger.info(f"Usuário {request.user} criou plano mensalista ID={plano.id}.")
            return redirect('planos:listar_planos_mensais')
    else:
        form = PlanoMensalForm()
    return render(request, 'planos/mensais/criar_plano_mensal.html', {'form': form})

@login_required(login_url='login_parkcontrol')
def criar_plano_diario(request):
    if request.method == 'POST':
        form = PlanoDiarioForm(request.POST)
        if form.is_valid():
            plano = form.save(commit=False)
            plano.tipo_plano = 'Diarista'
            plano.save()
            logger.info(f"Usuário {request.user} criou plano diarista ID={plano.id}.")
            return redirect('planos:listar_planos_diarios')
    else:
        form = PlanoDiarioForm()
    return render(request, 'planos/diarios/criar_plano_diario.html', {'form': form})

@login_required(login_url='login_parkcontrol')
def editar_plano_mensal(request, id):
    plano = get_object_or_404(Planos, id=id, tipo_plano='Mensalista')
    if request.method == 'POST':
        form = PlanoMensalForm(request.POST, instance=plano)
        if form.is_valid():
            form.save()
            logger.info(f"Usuário {request.user} editou plano mensalista ID={plano.id}.")
            return redirect('planos:listar_planos_mensais')
    else:
        form = PlanoMensalForm(instance=plano)
    return render(request, 'planos/mensais/editar_plano_mensal.html', {'form': form, 'plano': plano})

@login_required(login_url='login_parkcontrol')
def editar_plano_diario(request, id):
    plano = get_object_or_404(Planos, id=id, tipo_plano='Diarista')
    if request.method == 'POST':
        form = PlanoDiarioForm(request.POST, instance=plano)
        if form.is_valid():
            form.save()
            logger.info(f"Usuário {request.user} editou plano diarista ID={plano.id}.")
            return redirect('planos:listar_planos_diarios')
    else:
        form = PlanoDiarioForm(instance=plano)
    return render(request, 'planos/diarios/editar_plano_diario.html', {'form': form, 'plano': plano})

@login_required(login_url='login_parkcontrol')
def visualizar_plano_mensal(request, id):
    plano = get_object_or_404(Planos, id=id, tipo_plano='Mensalista')
    logger.info(f"Usuário {request.user} visualizou plano mensalista ID={plano.id}.")
    return render(request, 'planos/mensais/visualizar_plano_mensal.html', {'plano': plano})

@login_required(login_url='login_parkcontrol')
def visualizar_plano_diario(request, id):
    plano = get_object_or_404(Planos, id=id, tipo_plano='Diarista')
    logger.info(f"Usuário {request.user} visualizou plano diarista ID={plano.id}.")
    return render(request, 'planos/diarios/visualizar_plano_diario.html', {'plano': plano})

@login_required(login_url='login_parkcontrol')
def excluir_plano_mensal(request, id):
    plano = get_object_or_404(Planos, id=id, tipo_plano='Mensalista')
    if request.method == 'POST':
        plano.delete()
        logger.info(f"Usuário {request.user} excluiu plano mensalista ID={id}.")
        return redirect('planos:listar_planos_mensais')
    return render(request, 'planos/mensais/excluir_plano_mensal.html', {'plano': plano})

@login_required(login_url='login_parkcontrol')
def excluir_plano_diario(request, id):
    plano = get_object_or_404(Planos, id=id, tipo_plano='Diarista')
    if request.method == 'POST':
        plano.delete()
        logger.info(f"Usuário {request.user} excluiu plano diarista ID={id}.")
        return redirect('planos:listar_planos_diarios')
    return render(request, 'planos/diarios/excluir_plano_diario.html', {'plano': plano})
