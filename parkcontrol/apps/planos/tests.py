# /apps/planos/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal

# Importa o modelo que será testado
from .models import Planos

# Pega o modelo de usuário ativo no projeto (usuarios.Usuario)
User = get_user_model()


class PlanosMensaisCRUDTests(TestCase):
    """
    Conjunto de testes para verificar as operações de CRUD
    (Criação, Leitura, Edição, Exclusão) para Planos do tipo Mensalista.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Configura dados iniciais que serão usados por todos os testes na classe.
        É executado apenas uma vez, tornando os testes mais rápidos.
        """
        # Cria um usuário com perfil de Administrador para ter permissão de acesso.
        cls.user = User.objects.create_user(
            username='testadmin',
            password='testpassword',
            perfil_acesso='Administrador'
        )

        # Cria um plano mensal inicial que será usado nos testes de edição e exclusão.
        cls.plano_existente = Planos.objects.create(
            nome="Plano Mensal Básico",
            validade=30,
            tipo_plano='Mensalista',
            tipo_mensal='Mensal',
            valor=Decimal('120.00'),
            status='Ativo'
        )

    def setUp(self):
        """
        Configuração que é executada antes de CADA teste.
        Ideal para objetos que podem ser modificados, como o cliente de teste.
        """
        self.client = Client()
        # Faz o login do usuário de teste para todas as requisições.
        self.client.login(username='testadmin', password='testpassword')

    def test_criar_plano_mensal_com_dados_validos(self):
        """
        [Teste: Back-End] Criação de plano mensal.
        Verifica se um novo plano mensal pode ser criado com sucesso via POST.
        """
        # Dados do formulário para o novo plano
        form_data = {
            'nome': 'Plano Mensal Premium',
            'validade': 30,
            'descricao': 'Acesso total para mensalistas.',
            'status': 'Ativo',
            'valor': '199.90',
            'tipo_mensal': 'Mensal'
        }

        # Simula uma requisição POST para a URL de criação
        response = self.client.post(reverse('planos:criar_plano_mensal'), data=form_data)

        # 1. Verifica se a requisição redirecionou para a página de listagem
        self.assertEqual(response.status_code, 302, "A resposta deveria ser um redirecionamento.")
        self.assertRedirects(response, reverse('planos:listar_planos_mensais'))

        # 2. Verifica se o novo plano foi realmente criado no banco de dados
        #    (Esperamos 2 planos: 1 do setUpTestData + 1 criado agora)
        self.assertEqual(Planos.objects.count(), 2)
        
        # 3. Pega o plano recém-criado e verifica seus atributos
        novo_plano = Planos.objects.get(nome='Plano Mensal Premium')
        self.assertEqual(novo_plano.valor, Decimal('199.90'))
        self.assertEqual(novo_plano.tipo_plano, 'Mensalista')
        self.assertEqual(novo_plano.tipo_mensal, 'Mensal')

    def test_listar_planos_mensais(self):
        """
        [Teste: Back-End] Leitura/Listagem de planos mensais.
        Verifica se a página de listagem de planos mensais é renderizada
        corretamente e se contém o plano criado no setup.
        """
        # Simula uma requisição GET para a URL de listagem
        response = self.client.get(reverse('planos:listar_planos_mensais'))

        # 1. Verifica se a página foi carregada com sucesso
        self.assertEqual(response.status_code, 200)

        # 2. Verifica se o nome do nosso plano de teste aparece no conteúdo da página
        self.assertContains(response, self.plano_existente.nome)

        # 3. Verifica se o template correto foi utilizado
        self.assertTemplateUsed(response, 'planos/mensais/listar_planos_mensais.html')

    def test_editar_plano_mensal(self):
        """
        [Teste: Back-End] Edição de plano mensal.
        Verifica se um plano existente pode ser atualizado com sucesso.
        """
        # Novos dados para o formulário de edição
        dados_atualizados = {
            'nome': 'Plano Mensal Básico Editado',
            'validade': 45,
            'valor': '130.00',
            'status': 'Inativo',
            'tipo_mensal': 'Mensal'
        }

        # Simula uma requisição POST para a URL de edição do plano existente
        url = reverse('planos:editar_plano_mensal', kwargs={'id': self.plano_existente.id})
        response = self.client.post(url, data=dados_atualizados)

        # 1. Verifica o redirecionamento para a lista de planos
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('planos:listar_planos_mensais'))

        # 2. Recarrega o plano do banco de dados para pegar os valores atualizados
        self.plano_existente.refresh_from_db()

        # 3. Verifica se os campos foram de fato alterados
        self.assertEqual(self.plano_existente.nome, 'Plano Mensal Básico Editado')
        self.assertEqual(self.plano_existente.status, 'Inativo')
        self.assertEqual(self.plano_existente.valor, Decimal('130.00'))

    def test_excluir_plano_mensal(self):
        """
        [Teste: Back-End] Exclusão de plano mensal.
        Verifica se um plano pode ser excluído com sucesso.
        """
        # Conta quantos planos existem ANTES da exclusão
        total_planos_antes = Planos.objects.count()

        # URL para a exclusão do plano
        url = reverse('planos:excluir_plano_mensal', kwargs={'id': self.plano_existente.id})
        
        # A exclusão geralmente é feita via POST para segurança
        response = self.client.post(url)

        # 1. Verifica o redirecionamento após a exclusão
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('planos:listar_planos_mensais'))

        # 2. Verifica se o número de planos no banco diminuiu em 1
        self.assertEqual(Planos.objects.count(), total_planos_antes - 1)

        # 3. Verifica se o plano específico não existe mais
        with self.assertRaises(Planos.DoesNotExist):
            Planos.objects.get(id=self.plano_existente.id)
