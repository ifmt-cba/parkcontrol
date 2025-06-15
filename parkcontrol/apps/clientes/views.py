from django.shortcuts import get_object_or_404, redirect, render
from .forms import MensalistaForm, DiaristaForm
from .models import Mensalista, Diarista
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

def cadastrar_clientes_view(request):
    return render(request, 'clientes/cadastrar_cliente.html')

# cadastro de mensalista
def cadastro_mensalistas_view(request):
    if request.method == 'POST':
        form = MensalistaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Cliente mensalista cadastrado com sucesso!')
                form = MensalistaForm()   
            except Exception as e:
                messages.error(request, f'Erro interno ao salvar: {e}. Tente novamente.')
        else:
            messages.error(request, 'Erro ao cadastrar cliente. Verifique os dados informados.')
    else:
        form = MensalistaForm()
    return render(request, 'clientes/cadastro_mensalista.html', {'form': form})

#Cadastro de diarista
def cadastro_diaristas_view(request):
    if request.method == 'POST':
        form = DiaristaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Cliente diarista cadastrado com sucesso!')
                form = DiaristaForm()   
            except Exception as e:
                messages.error(request, f'Erro interno ao salvar: {e}. Tente novamente.')
        else:
            messages.error(request, 'Erro ao cadastrar cliente. Verifique os dados informados.')
    else:
        form = DiaristaForm()
    return render(request, 'clientes/cadastro_diarista.html', {'form': form})

#Visualizar cliente mensalista
def cliente_mensalista_view(request):
    mensalistas = Mensalista.objects.all() 

    query_nome = request.GET.get('nome', '') 
    query_placa = request.GET.get('placa', '')

    if query_nome:
        mensalistas = mensalistas.filter(nome__icontains=query_nome)
    
    if query_placa:
       mensalistas = mensalistas.filter(placa__icontains=query_placa) 
       
    return render(request, 'clientes/cliente_mensalista.html', {'mensalistas': mensalistas, 'query_nome': query_nome, 'query_placa': query_placa})

# Editar mensalista
def editar_mensalista_view(request, pk):
    mensalista = get_object_or_404(Mensalista, pk=pk)
    if request.method == 'POST':
        form = MensalistaForm(request.POST, instance=mensalista)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente mensalista atualizado com sucesso!')
            return redirect('clientes:editar_mensalista', pk=mensalista.pk) 
        else:
            messages.error(request, 'Erro ao atualizar cliente. Verifique os dados informados.')
    else:
        form = MensalistaForm(instance=mensalista) 
    return render(request, 'clientes/editar_mensalista.html', {'form': form, 'mensalista': mensalista})

#Visualizar cliente diarista
def cliente_diarista_view(request):
    diaristas = Diarista.objects.all()

    query_nome = request.GET.get('nome', '')
    query_placa = request.GET.get('placa', '')

    if query_nome:
        diaristas = diaristas.filter(nome__icontains=query_nome)
        
    if query_placa:
        diaristas = diaristas.filter(placa__icontains=query_placa)

    return render(request, 'clientes/cliente_diarista.html', {'diaristas': diaristas, 'query_nome': query_nome, 'query_placa': query_placa})

# Editar Diarista
def editar_diarista_view(request, pk):
    diarista = get_object_or_404(Diarista, pk=pk)
    if request.method == 'POST':
        form = DiaristaForm(request.POST, instance=diarista)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente diarista atualizado com sucesso!')
            return redirect('clientes:editar_diarista', pk=diarista.pk) 
        else:
            messages.error(request, 'Erro ao atualizar cliente. Verifique os dados informados.')
    else:
        form = DiaristaForm(instance=diarista) 
    return render(request, 'clientes/editar_diarista.html', {'form': form, 'diarista': diarista})

def is_admin(user):
    return user.is_superuser

# Excluir Mensalista
@user_passes_test(is_admin)
def excluir_mensalista_view(request, pk):
    mensalista = get_object_or_404(Mensalista, pk=pk)
    if request.method == 'POST':
        mensalista.delete()
        messages.success(request, 'Cliente mensalista excluído com sucesso!')
        return redirect('clientes:cliente_mensalista')  # ajuste para sua URL de listagem
    return render(request, 'clientes/confirmar_exclusao.html', {'cliente': mensalista, 'tipo': 'Mensalista'})

# Excluir Diarista
@user_passes_test(is_admin)
def excluir_diarista_view(request, pk):
    diarista = get_object_or_404(Diarista, pk=pk)
    if request.method == 'POST':
        diarista.delete()
        messages.success(request, 'Cliente diarista excluído com sucesso!')
        return redirect('clientes:cliente_diarista')  # ajuste para sua URL de listagem
    return render(request, 'clientes/confirmar_exclusao.html', {'cliente': diarista, 'tipo': 'Diarista'})

@user_passes_test(is_admin)
def inativar_diarista_view(request, pk):
    diarista = get_object_or_404(Diarista, pk=pk)
    diarista.ativo = False
    diarista.save()
    messages.success(request, 'Cliente diarista inativado com sucesso!')
    return redirect('clientes:cliente_diarista')

@user_passes_test(is_admin)
def ativar_diarista_view(request, pk):
    diarista = get_object_or_404(Diarista, pk=pk)
    diarista.ativo = True
    diarista.save()
    messages.success(request, 'Cliente diarista ativado com sucesso!')
    return redirect('clientes:cliente_diarista')

@user_passes_test(is_admin)
def ativar_mensalista_view(request, pk):
    mensalista = get_object_or_404(Mensalista, pk=pk)
    mensalista.ativo = True
    mensalista.save()
    messages.success(request, 'Cliente mensalista ativado com sucesso!')
    return redirect('clientes:cliente_mensalista')

@user_passes_test(is_admin)
def inativar_mensalista_view(request, pk):
    mensalista = get_object_or_404(Mensalista, pk=pk)
    mensalista.ativo = False
    mensalista.save()
    messages.success(request, 'Cliente mensalista inativado com sucesso!')
    return redirect('clientes:cliente_mensalista')