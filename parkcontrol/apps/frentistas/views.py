from django.shortcuts import render

def gerenciar_clientes_view(request):
    return render(request, 'frentistas/gerenciar_clientes.html')

def gerenciar_vagas_view(request):
    return render(request, 'frentistas/gerenciar_vagas.html')

def gerenciar_cobranca_diaria(request):
    return render(request, 'frentistas/gerenciar_cobranca_diaria.html')