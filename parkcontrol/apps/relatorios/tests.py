# /apps/relatorios/tests.py

import datetime
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

# Importe o modelo de usuário personalizado
# get_user_model() irá buscar 'usuarios.Usuario' como definido em settings.py
User = get_user_model()

# Modelos de outros apps necessários como dependência para os testes
from apps.planos.models import Planos
from apps.clientes.models import Mensalista
from apps.pagamentos.models import CobrancaMensalista, CobrancaDiaria

# Modelo do app atual que está sendo testado
from apps.relatorios.models import RelatorioFinanceiro


class RelatorioFinanceiroTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Usa setUpTestData para criar os dados de referência que não serão
        modificados durante os testes, o que é mais eficiente.
        """
        # 1. Cria um usuário (Contador) que será usado para criar o relatório.
        cls.user = User.objects.create_user(
            username='testcontador',
            password='testpassword',
            perfil_acesso='Contador'
        )

        # 2. Cria um Plano, que é um pré-requisito para o Mensalista.
        cls.plano_mensal = Planos.objects.create(
            nome="Plano Teste Mensal",
            validade=30,
            tipo_plano='Mensalista',
            status='Ativo',
            valor=Decimal('150.00')
        )

        # 3. Cria um cliente Mensalista.
        cls.cliente_mensalista = Mensalista.objects.create(
            nome="Cliente de Teste Mensal",
            telefone="(99) 99999-9999",
            email="cliente.teste@example.com",
            plano=cls.plano_mensal,
            placa="TES1T23", # Placa única no formato Mercosul
            ativo=True
        )

        # 4. Cria dados de teste para as cobranças que o relatório irá processar.
        #    Para campos com auto_now_add=True, criamos o objeto e depois
        #    atualizamos o campo manualmente para garantir a data correta no teste.

        # ----- Cobranças de Mensalistas -----
        cobranca_paga = CobrancaMensalista.objects.create(
            cliente_mensalista=cls.cliente_mensalista,
            data_vencimento=datetime.date(2023, 10, 25),
            mes_referencia="10/2023",
            valor_devido=Decimal('150.00'),
            valor_pago=Decimal('150.00'),
            status='pago'
        )
        cobranca_pendente = CobrancaMensalista.objects.create(
            cliente_mensalista=cls.cliente_mensalista,
            data_vencimento=datetime.date(2023, 10, 25),
            mes_referencia="10/2023-2",
            valor_devido=Decimal('200.00'),
            valor_pago=Decimal('0.00'),
            status='pendente'
        )

        # Atualiza os campos de data manualmente com timezone para evitar warnings.
        cobranca_paga.data_geracao = datetime.datetime(2023, 10, 5, tzinfo=timezone.utc)
        cobranca_paga.data_pagamento = datetime.datetime(2023, 10, 10, tzinfo=timezone.utc)
        cobranca_paga.save()

        cobranca_pendente.data_geracao = datetime.datetime(2023, 10, 15, tzinfo=timezone.utc)
        cobranca_pendente.save()


        # ----- Cobranças de Diaristas -----
        CobrancaDiaria.objects.create(
            placa="DIA1R10",
            data=datetime.date(2023, 10, 8),
            valor_total=Decimal('25.50'),
            status='Pago',
            horario_entrada=datetime.datetime(2023, 10, 8, 9, 0, 0, tzinfo=timezone.utc),
            horario_saida=datetime.datetime(2023, 10, 8, 11, 0, 0, tzinfo=timezone.utc),
        )

    def setUp(self):
        """
        Configuração que roda antes de CADA teste.
        """
        self.client = Client()
        self.client.login(username='testcontador', password='testpassword')


    def test_geracao_relatorio_financeiro_com_calculos_corretos(self):
        """
        [Teste: Back-End] Geração de relatório financeiro com filtros

        Verifica se a view 'criar_relatorio' processa os dados,
        calcula os totais corretamente e cria um novo objeto RelatorioFinanceiro.
        """
        form_data = {
            'nome': 'Relatório Final de Outubro',
            'data_inicio': '2023-10-01',
            'data_fim': '2023-10-31',
            'status': 'Finalizado'
        }
        response = self.client.post(reverse('relatorios:criar'), data=form_data)

        # Verifica se a requisição foi redirecionada com sucesso
        self.assertEqual(response.status_code, 302, "A resposta deveria ser um redirecionamento (302)")
        self.assertRedirects(response, reverse('relatorios:listar'))

        # Verifica se o relatório foi criado no banco
        self.assertEqual(RelatorioFinanceiro.objects.count(), 1, "Deveria haver 1 relatório criado no banco")
        relatorio_criado = RelatorioFinanceiro.objects.first()

        # Verifica se o relatório foi associado ao usuário correto
        self.assertEqual(relatorio_criado.criado_por, self.user)

        # Define os valores esperados com base nos dados de teste
        # Total Emitido: 150.00 (mensal) + 200.00 (mensal) + 25.50 (diaria) = 375.50
        total_emitido_esperado = Decimal('375.50')
        # Total Pago: 150.00 (mensal pago) + 25.50 (diaria paga) = 175.50
        total_pago_esperado = Decimal('175.50')
        # Total Inadimplente: 375.50 - 175.50 = 200.00
        total_inadimplente_esperado = Decimal('200.00')

        # Compara os valores calculados no relatório com os valores esperados
        self.assertEqual(relatorio_criado.total_emitido, total_emitido_esperado, "Cálculo do Total Emitido está incorreto.")
        self.assertEqual(relatorio_criado.total_pago, total_pago_esperado, "Cálculo do Total Pago está incorreto.")
        self.assertEqual(relatorio_criado.total_inadimplente, total_inadimplente_esperado, "Cálculo do Total Inadimplente está incorreto.")
