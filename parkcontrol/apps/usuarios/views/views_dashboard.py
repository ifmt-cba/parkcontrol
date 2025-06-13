from django.contrib.auth.decorators import login_required # Import login_required decorator
from django.contrib.auth.decorators import user_passes_test # Import user_passes_test decorator
from django.shortcuts import redirect, render # Import render function to render templates
from .views_autenticacao import is_administrador, is_contador, is_frentista # Import user access control functions

'''

    DASHBOARD

'''


@login_required(login_url='usuarios:login_parkcontrol')
def home_redirect(request):
    perfil = getattr(request.user, 'perfil_acesso', None)

    if perfil == 'Administrador':
        return redirect('usuarios:dashboard_administrador')
    elif perfil == 'Frentista':
        return redirect('usuarios:dashboard_frentista')
    elif perfil == 'Contador':
        return redirect('usuarios:dashboard_contador')
    else:
        # Fallback, caso o perfil não esteja definido
        return redirect('usuarios:login_parkcontrol')


# Dashboard for Administrador
@login_required(login_url='usuarios:login_parkcontrol')
@user_passes_test(is_administrador, login_url='usuarios:login_parkcontrol')
def dashboard_administrador(request):
    return render(request, 'usuarios/administrador/dashboard_administrador.html')

# Dashboard for Contador
@login_required(login_url='usuarios:login_parkcontrol')
@user_passes_test(is_contador, login_url='usuarios:login_parkcontrol')
def dashboard_contador(request):
    return render(request, 'usuarios/contador/dashboard_contador.html')

# Dashboard for Frentista
@login_required(login_url='usuarios:login_parkcontrol')
@user_passes_test(is_frentista, login_url='usuarios:login_parkcontrol')
def dashboard_frentista(request):
    return render(request, 'usuarios/frentista/dashboard_frentista.html')