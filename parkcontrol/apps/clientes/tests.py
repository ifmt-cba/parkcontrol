from django.test import TestCase
from django.urls import reverse
from apps.clientes.models import Diarista
from apps.usuarios.models import Usuario

class ListagemClientesDiaristasTest(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(username='admin', password='senha123', perfil_acesso='Administrador')
        self.client.login(username='admin', password='senha123')

        # Criando diaristas
        Diarista.objects.create(nome='João Diarista', placa='ABC1234')
        Diarista.objects.create(nome='Maria Diarista', placa='XYZ9876')

    def test_listagem_diaristas(self):
        response = self.client.get(reverse('clientes:cliente_diarista'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'João Diarista')
        self.assertContains(response, 'Maria Diarista')

        diaristas = response.context['diaristas']
        for diarista in diaristas:
            self.assertIsInstance(diarista, Diarista)
        self.assertIn('diaristas', response.context)
