from django.shortcuts import render

def gerencia_cliente(request):
    return render(request, 'usuarios/administrador/gerencia_cliente.html')