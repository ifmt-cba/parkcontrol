from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core import mail

User = get_user_model()

class RecuperacaoSenhaTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario = User.objects.create_user(
            username='admin',
            email='admin@email.com',
            first_name='Admin',
            password='admin123'
        )

    def test_recuperacao_com_dados_validos(self):
        response = self.client.post(reverse('recuperar_senha'), {
            'email': 'admin@email.com',
            'nome': 'Admin'
        })

        # Verifica que a mensagem de sucesso está na página
        self.assertContains(response, 'E-mail de redefinição enviado com sucesso.')

        # Verifica que um e-mail foi realmente enviado
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Redefinição de Senha', mail.outbox[0].subject)
        self.assertIn('admin@email.com', mail.outbox[0].to)

        #  http://localhost:8000/usuarios/recuperar-senha/