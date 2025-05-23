from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User # Import User model 
from django.contrib.auth import authenticate,logout,login # Import authenticate, logout, and login functions
from django.contrib.auth.decorators import login_required # Import login_required decorator

# Redirect to login page
def redirect_to_login(request):
    return redirect('login_parkcontrol')  

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
            return redirect('home_parkcontrol') # Redirect to home page after login
    else:
        # If the request method is GET, render the login page
        return render(request, 'usuarios/login.html') 

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
            return render(request, 'usuarios/register.html')
        
        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name)
        user.save()
        return redirect('register_parkcontrol') # Redirect to login page after registration
    else: 
        # If the request method is GET, render the registration page
        return render(request, 'usuarios/register.html')

# Logout page
def logout_parkcontrol(request):
    logout(request)    
    return render(request, 'usuarios/logout.html')


@login_required(login_url='login_parkcontrol') # Decorator to require login
# Home page
def home_parkcontrol(request):
    return render(request, 'usuarios/home.html')