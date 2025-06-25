from django.test import TestCase
from django.utils import timezone
from decimal import Decimal

from apps.clientes.models import Mensalista
from apps.pagamentos.models import CobrancaMensalista

class CobrancaMensalistaTestCase(TestCase):
    def setUp(self):
        self.mensalista = Mensalista.objects.create(
            nome='João da Silva',
            email='joao@example.com',
            telefone='(11) 99999-9999',
            placa='ABC1234',
            ativo=True
        )

        self.cobranca = CobrancaMensalista.objects.create(
            cliente_mensalista=self.mensalista,
            data_vencimento=timezone.now().date(),
            mes_referencia='06/2025',
            valor_devido=Decimal('150.00'),
            status='pendente'
        )

    def test_cobranca_criada_com_sucesso(self):
        self.assertEqual(CobrancaMensalista.objects.count(), 1)
        self.assertEqual(self.cobranca.valor_devido, Decimal('150.00'))
        self.assertFalse(self.cobranca.esta_paga())

    def test_status_pago_apos_pagamento(self):
        resultado = self.cobranca.salvar_pagamento(Decimal('150.00'))
        self.cobranca.refresh_from_db()
        self.assertTrue(self.cobranca.esta_paga())
        self.assertEqual(self.cobranca.valor_pago, Decimal('150.00'))
        self.assertIn('paga integralmente', resultado.lower())

    def test_pagamento_parcial_nao_muda_status(self):
        resultado = self.cobranca.salvar_pagamento(Decimal('50.00'))
        self.cobranca.refresh_from_db()
        self.assertEqual(self.cobranca.valor_pago, Decimal('0.00')) 
        self.assertEqual(self.cobranca.status, 'pendente')

    def test_esta_vencida(self):
        self.cobranca.data_vencimento = timezone.now().date() - timezone.timedelta(days=1)
        self.cobranca.save()
        self.assertTrue(self.cobranca.esta_vencida())

    def test_calculo_saldo(self):
        self.assertEqual(self.cobranca.calcular_saldo_pendente(), Decimal('150.00'))

