from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import MensalistaForm, DiaristaForm
from .models import Mensalista, Diarista
from django.contrib import messages

def cadastrar_clientes_view(request):
    return render(request, 'clientes/cadastrar_cliente.html')

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

def cliente_mensalista_view(request):
    mensalistas = Mensalista.objects.all() 

    query_nome = request.GET.get('nome', '') 
    query_placa = request.GET.get('placa', '')

    if query_nome:
        mensalistas = mensalistas.filter(nome__icontains=query_nome)
    
    if query_placa:
       mensalistas = mensalistas.filter(placa__icontains=query_placa) 
       
    return render(request, 'clientes/cliente_mensalista.html', {'mensalistas': mensalistas, 'query_nome': query_nome, 'query_placa': query_placa})

def editar_mensalista_view(request, pk):
    mensalista = get_object_or_404(Mensalista, pk=pk)
    if request.method == 'POST':
        form = MensalistaForm(request.POST, instance=mensalista)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente mensalista atualizado com sucesso!')
            return redirect('cliente_mensalista') 
        else:
            messages.error(request, 'Erro ao atualizar cliente. Verifique os dados informados.')
    else:
        form = MensalistaForm(instance=mensalista) 
    return render(request, 'clientes/editar_mensalista.html', {'form': form, 'mensalista': mensalista})

def cliente_diarista_view(request):
    diaristas = Diarista.objects.all()

    query_nome = request.GET.get('nome', '')
    query_placa = request.GET.get('placa', '')

    if query_nome:
        diaristas = diaristas.filter(nome__icontains=query_nome)
        
    if query_placa:
        diaristas = diaristas.filter(placa__icontains=query_placa)

    return render(request, 'clientes/cliente_diarista.html', {'diaristas': diaristas, 'query_nome': query_nome, 'query_placa': query_placa})

def editar_diarista_view(request, pk):
    diarista = get_object_or_404(Diarista, pk=pk)
    if request.method == 'POST':
        form = DiaristaForm(request.POST, instance=diarista)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente diarista atualizado com sucesso!')
            return redirect('clientes:cliente_diarista') 
        else:
            messages.error(request, 'Erro ao atualizar cliente. Verifique os dados informados.')
    else:
        form = DiaristaForm(instance=diarista) 
    return render(request, 'clientes/editar_diarista.html', {'form': form, 'diarista': diarista})