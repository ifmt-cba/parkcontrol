import logging
from django.shortcuts import get_object_or_404, redirect, render
from apps.usuarios.views.views_autenticacao import is_administrador
from .forms import MensalistaForm, DiaristaForm
from .models import Mensalista, Diarista
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

logger = logging.getLogger('clientes')  # logger para o app clientes

@login_required(login_url='login_parkcontrol')
def cadastrar_clientes_view(request):
    return render(request, 'clientes/cadastrar_cliente.html')

@login_required(login_url='login_parkcontrol')
def cadastro_mensalistas_view(request):
    if request.method == 'POST':
        form = MensalistaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Cliente mensalista cadastrado com sucesso!')
                logger.info(f"Cliente mensalista cadastrado: {form.cleaned_data.get('nome', 'Nome não disponível')}")
                form = MensalistaForm()
            except Exception as e:
                messages.error(request, f'Erro interno ao salvar: {e}. Tente novamente.')
                logger.error(f"Erro ao salvar cliente mensalista: {e}", exc_info=True)
        else:
            messages.error(request, 'Erro ao cadastrar cliente. Verifique os dados informados.')
            logger.warning("Formulário inválido no cadastro de mensalista.")
    else:
        form = MensalistaForm()
    return render(request, 'clientes/cadastro_mensalista.html', {'form': form})

@login_required(login_url='login_parkcontrol')
def cadastro_diaristas_view(request):
    if request.method == 'POST':
        form = DiaristaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Cliente diarista cadastrado com sucesso!')
                logger.info(f"Cliente diarista cadastrado: {form.cleaned_data.get('nome', 'Nome não disponível')}")
                form = DiaristaForm()
            except Exception as e:
                messages.error(request, f'Erro interno ao salvar: {e}. Tente novamente.')
                logger.error(f"Erro ao salvar cliente diarista: {e}", exc_info=True)
        else:
            messages.error(request, 'Erro ao cadastrar cliente. Verifique os dados informados.')
            logger.warning("Formulário inválido no cadastro de diarista.")
    else:
        form = DiaristaForm()
    return render(request, 'clientes/cadastro_diarista.html', {'form': form})

@login_required(login_url='login_parkcontrol')
def cliente_mensalista_view(request):
    mensalistas = Mensalista.objects.all()
    query_nome = request.GET.get('nome', '')
    query_placa = request.GET.get('placa', '')

    if query_nome:
        mensalistas = mensalistas.filter(nome__icontains=query_nome)
    if query_placa:
        mensalistas = mensalistas.filter(placa__icontains=query_placa)
    
    logger.info(f"Visualização lista mensalistas - filtros: nome='{query_nome}', placa='{query_placa}'")

    return render(request, 'clientes/cliente_mensalista.html', {'mensalistas': mensalistas, 'query_nome': query_nome, 'query_placa': query_placa})

@login_required(login_url='login_parkcontrol')
def editar_mensalista_view(request, pk):
    mensalista = get_object_or_404(Mensalista, pk=pk)
    if request.method == 'POST':
        form = MensalistaForm(request.POST, instance=mensalista)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente mensalista atualizado com sucesso!')
            logger.info(f"Cliente mensalista atualizado: ID={mensalista.pk}, Nome={mensalista.nome}")
            return redirect('clientes:editar_mensalista', pk=mensalista.pk)
        else:
            messages.error(request, 'Erro ao atualizar cliente. Verifique os dados informados.')
            logger.warning(f"Falha ao atualizar mensalista ID={mensalista.pk} - dados inválidos.")
    else:
        form = MensalistaForm(instance=mensalista)
    return render(request, 'clientes/editar_mensalista.html', {'form': form, 'mensalista': mensalista})

@login_required(login_url='login_parkcontrol')
def cliente_diarista_view(request):
    diaristas = Diarista.objects.all()
    query_nome = request.GET.get('nome', '')
    query_placa = request.GET.get('placa', '')

    if query_nome:
        diaristas = diaristas.filter(nome__icontains=query_nome)
    if query_placa:
        diaristas = diaristas.filter(placa__icontains=query_placa)
    
    logger.info(f"Visualização lista diaristas - filtros: nome='{query_nome}', placa='{query_placa}'")

    return render(request, 'clientes/cliente_diarista.html', {'diaristas': diaristas, 'query_nome': query_nome, 'query_placa': query_placa})

@login_required(login_url='login_parkcontrol')
def editar_diarista_view(request, pk):
    diarista = get_object_or_404(Diarista, pk=pk)
    if request.method == 'POST':
        form = DiaristaForm(request.POST, instance=diarista)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente diarista atualizado com sucesso!')
            logger.info(f"Cliente diarista atualizado: ID={diarista.pk}, Nome={diarista.nome}")
            return redirect('clientes:editar_diarista', pk=diarista.pk)
        else:
            messages.error(request, 'Erro ao atualizar cliente. Verifique os dados informados.')
            logger.warning(f"Falha ao atualizar diarista ID={diarista.pk} - dados inválidos.")
    else:
        form = DiaristaForm(instance=diarista)
    return render(request, 'clientes/editar_diarista.html', {'form': form, 'diarista': diarista})

@login_required(login_url='login_parkcontrol')
@user_passes_test(is_administrador)
def excluir_mensalista_view(request, pk):
    mensalista = get_object_or_404(Mensalista, pk=pk)
    if request.method == 'POST':
        mensalista.delete()
        messages.success(request, 'Cliente mensalista excluído com sucesso!')
        logger.info(f"Cliente mensalista excluído: ID={pk}, Nome={mensalista.nome}")
        return redirect('clientes:cliente_mensalista')
    return render(request, 'clientes/confirmar_exclusao.html', {'cliente': mensalista, 'tipo': 'Mensalista'})

@login_required(login_url='login_parkcontrol')
@user_passes_test(is_administrador)
def excluir_diarista_view(request, pk):
    diarista = get_object_or_404(Diarista, pk=pk)
    if request.method == 'POST':
        diarista.delete()
        messages.success(request, 'Cliente diarista excluído com sucesso!')
        logger.info(f"Cliente diarista excluído: ID={pk}, Nome={diarista.nome}")
        return redirect('clientes:cliente_diarista')
    return render(request, 'clientes/confirmar_exclusao.html', {'cliente': diarista, 'tipo': 'Diarista'})

@login_required(login_url='login_parkcontrol')
@user_passes_test(is_administrador)
def inativar_diarista_view(request, pk):
    diarista = get_object_or_404(Diarista, pk=pk)
    diarista.ativo = False
    diarista.save()
    messages.success(request, 'Cliente diarista inativado com sucesso!')
    logger.info(f"Cliente diarista inativado: ID={pk}, Nome={diarista.nome}")
    return redirect('clientes:cliente_diarista')

@login_required(login_url='login_parkcontrol')
@user_passes_test(is_administrador)
def ativar_diarista_view(request, pk):
    diarista = get_object_or_404(Diarista, pk=pk)
    diarista.ativo = True
    diarista.save()
    messages.success(request, 'Cliente diarista ativado com sucesso!')
    logger.info(f"Cliente diarista ativado: ID={pk}, Nome={diarista.nome}")
    return redirect('clientes:cliente_diarista')

@login_required(login_url='login_parkcontrol')
@user_passes_test(is_administrador)
def ativar_mensalista_view(request, pk):
    mensalista = get_object_or_404(Mensalista, pk=pk)
    mensalista.ativo = True
    mensalista.save()
    messages.success(request, 'Cliente mensalista ativado com sucesso!')
    logger.info(f"Cliente mensalista ativado: ID={pk}, Nome={mensalista.nome}")
    return redirect('clientes:cliente_mensalista')

@login_required(login_url='login_parkcontrol')
@user_passes_test(is_administrador)
def inativar_mensalista_view(request, pk):
    mensalista = get_object_or_404(Mensalista, pk=pk)
    mensalista.ativo = False
    mensalista.save()
    messages.success(request, 'Cliente mensalista inativado com sucesso!')
    logger.info(f"Cliente mensalista inativado: ID={pk}, Nome={mensalista.nome}")
    return redirect('clientes:cliente_mensalista')
