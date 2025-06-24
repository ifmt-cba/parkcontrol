from django.shortcuts import render
from apps.vagas.models import Vaga

def historico(request):
    return render(request, 'usuarios/administrador/historico/dashboard_historico.html')

def historico_vagas(request):
    historicos = Vaga.historico.all().order_by('-history_date')
    return render(request, 'usuarios/administrador/historico/historico_vagas.html', {'historicos': historicos})