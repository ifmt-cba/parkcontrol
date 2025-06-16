from django.shortcuts import render


def manutencao_dashboard(request):
    return render(request, 'manutencao/manutencao.html')