from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User # Import User model 
from django.contrib.auth import authenticate,logout,login # Import authenticate, logout, and login functions
from django.contrib.auth.decorators import login_required # Import login_required decorator
from django.contrib import messages # Import messages framework for displaying messages
from django.contrib.auth.decorators import user_passes_test # Import user_passes_test decorator


# Redirect to login page
def redirect_to_login(request):
    return redirect('login_parkcontrol')  

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
def login_parkcontrol(request):

    # Check if the user is already authenticated
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        # Check if the user is authenticated
        if user is not None:
            login(request, user)
             # Redirecionamento por perfil
            perfil = getattr(user, 'perfil_acesso', None)

            if perfil == 'Administrador':
                return redirect('dashboard_administrador')
            elif perfil == 'Frentista':
                return redirect('dashboard_frentista')
            elif perfil == 'Contador':
                return redirect('dashboard_contador')
            else:
                messages.warning(request, 'Perfil de acesso não identificado.')
                return redirect('login_parkcontrol')
        else:
            messages.error(request, 'E-mail ou senha inválidos.')
            return render(request, 'autenticacao/login.html')
    else:
        # If the request method is GET, render the login page
        return render(request, 'autenticacao/login.html') 

def logout_parkcontrol(request):
    logout(request)    
    return render(request, 'autenticacao/logout.html')

