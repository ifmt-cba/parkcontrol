from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .views_autenticacao import is_administrador
from apps.usuarios.models import Usuario
from django.contrib import messages


@login_required(login_url='usuarios:login_parkcontrol')
@user_passes_test(is_administrador, login_url='usuarios:login_parkcontrol')
def gerencia_usuarios(request):
    usuarios = Usuario.objects.all().order_by('id')

    # Filtros
    search_nome = request.GET.get('nome')
    search_email = request.GET.get('email')
    filtro_perfil = request.GET.get('perfil')

    if search_nome:
        usuarios = usuarios.filter(first_name__icontains=search_nome)

    if search_email:
        usuarios = usuarios.filter(email__icontains=search_email)

    if filtro_perfil and filtro_perfil != 'Todos':
        usuarios = usuarios.filter(perfil_acesso=filtro_perfil)

    return render(request, 'usuarios/administrador/gerencia_usuario.html', {
        'usuarios': usuarios,
        'search_nome': search_nome,
        'search_email': search_email,
        'filtro_perfil': filtro_perfil,
    })



@login_required(login_url='usuarios:login_parkcontrol')
@user_passes_test(is_administrador, login_url='usuarios:login_parkcontrol')
def register_parkcontrol(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # email
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        perfil = request.POST.get('perfil_acesso')

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "Já existe um usuário com este e-mail.")
            return redirect('usuarios:register_parkcontrol')

        user = Usuario.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            perfil_acesso=perfil
        )
        user.save()
        messages.success(request, f"Usuário {user.first_name} ({user.perfil_acesso}) cadastrado com sucesso!")
        return redirect('usuarios:gerencia_usuarios')

    return render(request, 'usuarios/administrador/register.html')




# EDITAR USUÁRIO
@login_required(login_url='usuarios:login_parkcontrol')
@user_passes_test(is_administrador, login_url='usuarios:login_parkcontrol')
def editar_usuario(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)

    if request.method == 'POST':
        usuario.username = request.POST.get('username')
        usuario.email = request.POST.get('email')
        usuario.first_name = request.POST.get('first_name')
        usuario.perfil_acesso = request.POST.get('perfil_acesso')

        usuario.save()
        messages.success(request, f"Usuário {usuario.first_name} atualizado com sucesso!")
        return redirect('usuarios:gerencia_usuarios')

    return render(request, 'usuarios/administrador/editar_usuario.html', {
        'usuario': usuario
    })


# EXCLUIR USUÁRIO
@login_required(login_url='usuarios:login_parkcontrol')
@user_passes_test(is_administrador, login_url='usuarios:login_parkcontrol')
def excluir_usuario(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    usuario.delete()
    messages.success(request, f"Usuário {usuario.first_name} excluído com sucesso!")
    return redirect('usuarios:gerencia_usuarios')
