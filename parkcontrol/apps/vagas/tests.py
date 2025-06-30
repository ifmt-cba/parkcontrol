from django.test import TestCase
from django.urls import reverse
from apps.vagas.models import Vaga, EntradaVeiculo, SaidaVeiculo
from apps.clientes.models import Mensalista, Diarista
from django.utils import timezone

class EntradaSaidaVeiculoTest(TestCase):
    def setUp(self):
        self.vaga = Vaga.objects.create(numero='1', status='Livre')
        self.diarista = Diarista.objects.create(nome='João Diarista', placa='ABC1D23')
        self.mensalista = Mensalista.objects.create(nome='Maria Mensalista', placa='XYZ1A23', telefone='(65) 99999-9999', email='maria@email.com', plano=None)

    def test_registrar_entrada_diarista(self):
        data = {
            'placa': self.diarista.placa,
            'nome': self.diarista.nome,
            'vaga': self.vaga.id,
            'tipo_cliente': 'Diarista',
        }
        response = self.client.post(reverse('vagas:registrar_entrada'), data)
        self.assertEqual(response.status_code, 302)
        entrada = EntradaVeiculo.objects.get(placa=self.diarista.placa)
        self.assertEqual(entrada.nome, self.diarista.nome)
        self.assertEqual(entrada.vaga, self.vaga)
        self.vaga.refresh_from_db()
        self.assertEqual(self.vaga.status, 'Ocupada')

    def test_registrar_saida_diarista(self):
        entrada = EntradaVeiculo.objects.create(
            nome=self.diarista.nome,
            tipo_cliente='Diarista',
            placa=self.diarista.placa,
            vaga=self.vaga,
            horario_entrada=timezone.now() - timezone.timedelta(hours=2)
        )
        self.vaga.status = 'Ocupada'
        self.vaga.save()
        data = {'placa': self.diarista.placa}
        response = self.client.post(reverse('vagas:registrar_saida'), data)
        self.assertEqual(response.status_code, 302)
        saida = SaidaVeiculo.objects.get(entrada=entrada)
        self.assertEqual(saida.placa, self.diarista.placa)
        self.assertEqual(saida.entrada, entrada)
        self.vaga.refresh_from_db()
        self.assertEqual(self.vaga.status, 'Livre')

    def test_registrar_saida_mensalista(self):
        entrada = EntradaVeiculo.objects.create(
            nome=self.mensalista.nome,
            tipo_cliente='Mensalista',
            placa=self.mensalista.placa,
            vaga=self.vaga,
            horario_entrada=timezone.now() - timezone.timedelta(hours=3)
        )
        self.vaga.status = 'Ocupada'
        self.vaga.save()
        data = {'placa': self.mensalista.placa}
        response = self.client.post(reverse('vagas:registrar_saida'), data)
        self.assertEqual(response.status_code, 302)
        saida = SaidaVeiculo.objects.get(entrada=entrada)
        self.assertEqual(saida.placa, self.mensalista.placa)
        self.assertEqual(saida.tipo_cliente, 'Mensalista')
        self.assertEqual(saida.entrada, entrada)
        self.vaga.refresh_from_db()
        self.assertEqual(self.vaga.status, 'Livre')
