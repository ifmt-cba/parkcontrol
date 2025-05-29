from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .views_autenticacao import is_administrador
from apps.usuarios.models import Usuario
from django.contrib import messages


@login_required(login_url='login_parkcontrol')
@user_passes_test(is_administrador, login_url='login_parkcontrol')
def gerencia_usuarios(request):
    usuarios = Usuario.objects.all().order_by('id')  # busca todos os usuários
    return render(request, 'usuarios/administrador/gerencia_usuario.html', {
        'usuarios': usuarios
    })


@login_required(login_url='login_parkcontrol')
@user_passes_test(is_administrador, login_url='login_parkcontrol')
def register_parkcontrol(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # matrícula ou ID interno
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        perfil = request.POST.get('perfil_acesso')

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "Já existe um usuário com este e-mail.")
            return redirect('register_parkcontrol')

        user = Usuario.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            perfil_acesso=perfil
        )
        user.save()
        messages.success(request, f"Usuário {user.first_name} ({user.perfil_acesso}) cadastrado com sucesso!")
        return redirect('gerencia_usuarios')

    return render(request, 'usuarios/administrador/register.html')