from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.vagas.models import Vaga, SolicitacaoManutencao

User = get_user_model()

class ManutencaoTests(TestCase):
    def setUp(self):
        # Cria um usuário administrador para realizar os testes autenticados
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@email.com',
            password='admin123',
            perfil_acesso='Administrador',
            first_name='Admin'
        )

        # Cria uma vaga para associar à solicitação
        self.vaga = Vaga.objects.create(
            numero='A01',
            status='Livre'
        )

        # Cria cliente para fazer requisições autenticadas
        self.client = Client()
        self.client.login(username='admin', password='admin123')

    def test_criacao_solicitacao_manutencao(self):
        """Verifica se uma solicitação de manutenção pode ser criada com sucesso"""
        solicitacao = SolicitacaoManutencao.objects.create(
            numero_vaga=self.vaga,
            descricao='Luz queimada na vaga',
            solicitante=self.admin
        )

        self.assertEqual(solicitacao.numero_vaga.numero, 'A01')
        self.assertFalse(solicitacao.resolvido)
        self.assertEqual(solicitacao.descricao, 'Luz queimada na vaga')

    def test_encerramento_de_solicitacao(self):
        """Verifica se o status de uma solicitação muda para resolvido e a vaga volta para Livre"""
        solicitacao = SolicitacaoManutencao.objects.create(
            numero_vaga=self.vaga,
            descricao='Buraco no piso',
            solicitante=self.admin,
            resolvido=False
        )

        # Simula a atualização da vaga para manutenção
        self.vaga.status = 'Manutenção'
        self.vaga.save()

        # Encerrar a solicitação via lógica da view
        url = reverse('manutencao:encerrar_solicitacao', args=[solicitacao.id])
        response = self.client.get(url, follow=True)

        # Atualiza os objetos do banco
        solicitacao.refresh_from_db()
        self.vaga.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(solicitacao.resolvido)
        self.assertEqual(self.vaga.status, 'Livre')
