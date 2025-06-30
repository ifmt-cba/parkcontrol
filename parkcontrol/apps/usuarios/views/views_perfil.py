from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from apps.usuarios.models import Usuario
import logging

logger = logging.getLogger('usuarios')


# Página principal do perfil
@login_required(login_url='usuarios:login_parkcontrol')
def perfil_usuario(request):
    logger.info(f"Usuário {request.user.username} acessou a página de perfil.")
    return render(request, 'perfil/perfil_usuario.html')


# View para editar nome e e-mail
@login_required(login_url='usuarios:login_parkcontrol')
def editar_perfil_usuario(request):
    if request.method == 'POST':
        user = request.user
        nome = request.POST.get('first_name')
        email = request.POST.get('email')

        if Usuario.objects.exclude(id=user.id).filter(email=email).exists():
            logger.warning(f"Usuário {user.username} tentou alterar para um e-mail já existente: {email}")
            messages.error(request, 'Já existe um usuário com este e-mail.')
            return redirect('usuarios:perfil_usuario')

        user.first_name = nome
        user.email = email
        user.save()
        logger.info(f"Usuário {user.username} atualizou seu perfil (nome/email).")
        messages.success(request, 'Perfil atualizado com sucesso.')
        return redirect('usuarios:perfil_usuario')
    else:
        return redirect('usuarios:perfil_usuario')


# View para alterar senha
@login_required(login_url='usuarios:login_parkcontrol')
def alterar_senha_usuario(request):
    if request.method == 'POST':
        user = request.user
        senha_atual = request.POST.get('senha_atual')
        nova_senha = request.POST.get('nova_senha')
        confirmar = request.POST.get('confirmar_senha')

        if not check_password(senha_atual, user.password):
            logger.warning(f"Usuário {user.username} forneceu senha atual incorreta ao tentar trocar a senha.")
            messages.error(request, 'Senha atual incorreta.')
            return redirect('usuarios:perfil_usuario')

        if nova_senha != confirmar:
            logger.warning(f"Usuário {user.username} informou confirmação de senha diferente.")
            messages.error(request, 'A nova senha e a confirmação não coincidem.')
            return redirect('usuarios:perfil_usuario')

        if len(nova_senha) < 8:
            logger.warning(f"Usuário {user.username} tentou definir uma senha menor que 8 caracteres.")
            messages.warning(request, 'A nova senha deve conter pelo menos 8 caracteres.')
            return redirect('usuarios:perfil_usuario')

        user.set_password(nova_senha)
        user.save()
        update_session_auth_hash(request, user)  # mantém o login ativo após trocar a senha
        logger.info(f"Usuário {user.username} alterou a senha com sucesso.")
        messages.success(request, 'Senha alterada com sucesso.')
        return redirect('usuarios:perfil_usuario')

    return redirect('usuarios:perfil_usuario')
