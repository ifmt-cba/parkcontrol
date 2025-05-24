from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse

User = get_user_model()

def recuperar_senha(request):
    mensagem = ''
    status = ''

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        nome = request.POST.get('nome', '').strip()

        qs_email = User.objects.filter(email=email)
        if not qs_email.exists():
            mensagem = 'E-mail não cadastrado.'
            status = 'erro'
        else:
            user = qs_email.filter(first_name=nome).first()
            if not user:
                mensagem = 'Nome não corresponde ao e-mail informado.'
                status = 'erro'
            else:
                # ✅ Gera token e link
                token = default_token_generator.make_token(user)
                uid = user.pk
                reset_path = reverse(
                    'password_reset_confirm',
                    kwargs={'uidb64': uid, 'token': token}
                )
                reset_link = request.build_absolute_uri(reset_path)

                # ✅ Envia e-mail
                send_mail(
                    subject='Redefinição de Senha – ParkControl',
                    message=(
                        f'Olá {user.first_name},\n\n'
                        f'Use este link para redefinir sua senha:\n{reset_link}\n\n'
                        'Se não foi você, ignore esta mensagem.'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )

                mensagem = 'E-mail de redefinição enviado com sucesso.'
                status = 'sucesso'

    return render(request, 'usuarios/recuperar-senha.html', {
        'mensagem': mensagem,
        'status': status,
    })
