from django.shortcuts import render

def relatorios(request):
    return render(request, 'relatorios.html')