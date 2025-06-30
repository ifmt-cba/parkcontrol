from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class LoginUsuarioTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario = User.objects.create_user(
            username='admin',
            email='admin@email.com',
            password='admin123'
        )

    def test_login_com_credenciais_validas(self):
        response = self.client.post(reverse('usuarios:login_parkcontrol'), {
            'username': 'admin',
            'password': 'admin123'
        })

        # Redireciona para alguma dashboard (como administrador)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('usuarios:dashboard_administrador'))

    def test_login_com_credenciais_invalidas(self):
        response = self.client.post(reverse('usuarios:login_parkcontrol'), {
            'username': 'admin',
            'password': 'senhaerrada'
        })

        # Página recarrega com erro
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'E-mail ou senha inválidos.')
