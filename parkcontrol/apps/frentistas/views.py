from django.shortcuts import render

def home_frentista(request):
    return render(request, 'frentistas/home_frentista.html')

def gerenciar_clientes_view(request):
    return render(request, 'frentistas/gerenciar_clientes.html')

def gerenciar_vagas_view(request):
    return render(request, 'frentistas/gerenciar_vagas.html')