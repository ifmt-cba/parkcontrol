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

#Registration page
def register_parkcontrol(request):
    # Check if the user is already authenticated
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')

        # Check if the user already exists
        user = User.objects.filter(username=username).first()

        if user:
            return render(request, 'autenticacao/register.html')
        
        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name)
        user.save()
        return redirect('register_parkcontrol') # Redirect to login page after registration
    else: 
        # If the request method is GET, render the registration page
        return render(request, 'autenticacao/register.html')

# Logout page
def logout_parkcontrol(request):
    logout(request)    
    return render(request, 'autenticacao/logout.html')


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