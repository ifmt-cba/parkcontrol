from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User # Import User model 
from django.contrib.auth import authenticate,logout,login # Import authenticate, logout, and login functions
from django.contrib.auth.decorators import login_required # Import login_required decorator
from django.contrib import messages # Import messages framework for displaying messages
from django.contrib.auth.decorators import user_passes_test # Import user_passes_test decorator
import logging

logger = logging.getLogger('usuarios')

# Redirect to login page
def redirect_to_login(request):
    return redirect('usuarios:login_parkcontrol')  

'''

    USER ACCESS CONTROL

'''
def is_administrador(user):
    return user.is_authenticated and getattr(user, 'perfil_acesso', None) == 'Administrador'

def is_contador(user):
    return user.is_authenticated and getattr(user, 'perfil_acesso', None) == 'Contador'

def is_frentista(user):
    return user.is_authenticated and getattr(user, 'perfil_acesso', None) == 'Frentista'


'''

    AUTENTICATION 

'''
# Login page
# Redireciona para o login
def redirect_to_login(request):
    logger.info(f"Usuário não autenticado redirecionado para login.")
    return redirect('usuarios:login_parkcontrol')


# LOGIN
def login_parkcontrol(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            perfil = getattr(user, 'perfil_acesso', None)
            logger.info(f"Usuário {username} autenticado com sucesso. Perfil: {perfil}")

            if perfil == 'Administrador':
                return redirect('usuarios:dashboard_administrador')
            elif perfil == 'Frentista':
                return redirect('usuarios:dashboard_frentista')
            elif perfil == 'Contador':
                return redirect('usuarios:dashboard_contador')
            else:
                logger.warning(f"Usuário {username} autenticado, mas sem perfil válido.")
                messages.warning(request, 'Perfil de acesso não identificado.')
                return redirect('usuarios:login_parkcontrol')
        else:
            logger.warning(f"Tentativa de login falhou para usuário: {username}")
            messages.error(request, 'E-mail ou senha inválidos.')
            return render(request, 'autenticacao/login.html')
    else:
        logger.debug("Página de login renderizada via GET")
        return render(request, 'autenticacao/login.html')


# LOGOUT
def logout_parkcontrol(request):
    logger.info(f"Usuário {request.user} fez logout.")
    logout(request)
    return render(request, 'autenticacao/logout.html')


# DASHBOARDS
@login_required(login_url='login_parkcontrol')
@user_passes_test(is_administrador, login_url='login_parkcontrol')
def dashboard_administrador(request):
    logger.info(f"Dashboard administrador acessado por {request.user}")
    return render(request, 'usuarios/administrador/dashboard_administrador.html')

@login_required(login_url='login_parkcontrol')
@user_passes_test(is_contador, login_url='login_parkcontrol')
def dashboard_contador(request):
    logger.info(f"Dashboard contador acessado por {request.user}")
    return render(request, 'usuarios/contador/dashboard_contador.html')

@login_required(login_url='login_parkcontrol')
@user_passes_test(is_frentista, login_url='login_parkcontrol')
def dashboard_frentista(request):
    logger.info(f"Dashboard frentista acessado por {request.user}")
    return render(request, 'usuarios/frentista/dashboard_frentista.html')


# Recuperação de senha
def recuperar_senha(request):
    logger.debug("Página de recuperação de senha acessada.")
    return render(request, 'autenticacao/recuperar-senha.html')
