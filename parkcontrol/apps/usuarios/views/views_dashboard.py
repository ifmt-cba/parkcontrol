from django.contrib.auth.decorators import login_required # Import login_required decorator
from django.contrib.auth.decorators import user_passes_test # Import user_passes_test decorator
from django.shortcuts import render # Import render function to render templates
from .views_autenticacao import is_administrador, is_contador, is_frentista # Import user access control functions

'''

    DASHBOARD

'''

# Dashboard for Administrador
@login_required(login_url='login_parkcontrol')
@user_passes_test(is_administrador, login_url='login_parkcontrol')
def dashboard_administrador(request):
    return render(request, 'usuarios/administrador/dashboard_administrador.html')

# Dashboard for Contador
@login_required(login_url='login_parkcontrol')
@user_passes_test(is_contador, login_url='login_parkcontrol')
def dashboard_contador(request):
    return render(request, 'usuarios/contador/dashboard_contador.html')

# Dashboard for Frentista
@login_required(login_url='login_parkcontrol')
@user_passes_test(is_frentista, login_url='login_parkcontrol')
def dashboard_frentista(request):
    return render(request, 'usuarios/frentista/dashboard_frentista.html')