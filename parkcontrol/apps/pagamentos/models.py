from django.db import models
from django.utils import timezone
from decimal import Decimal
import math

from apps.clientes.models import Mensalista

class CobrancaDiaria(models.Model):
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Pago', 'Pago')
    ]

    placa = models.CharField(max_length=10)
    nome = models.CharField(max_length=100, blank=True, null=True)
    data = models.DateField(default=timezone.now)
    valor_total = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pendente')

    horario_entrada = models.DateTimeField()
    horario_saida = models.DateTimeField()

    def __str__(self):
        return f'{self.placa} - {self.data} - {self.status}'
    
class cliente_mensalista(models.Model):
        STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
    ]

        cliente_mensalista = models.ForeignKey(Mensalista, on_delete=models.CASCADE, verbose_name="Cliente Mensalista")
    
        data_geracao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Geração")
        data_vencimento = models.DateField(verbose_name="Data de Vencimento")
        mes_referencia = models.CharField(max_length=7, verbose_name="Mês de Referência (MM/AAAA)", help_text="Para cobranças mensais, ex: 05/2025")

        valor_devido = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Devido")
        valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name="Valor Pago")
        status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente', verbose_name="Status")
        data_pagamento = models.DateTimeField(null=True, blank=True, verbose_name="Data do Pagamento")
    
        descricao = models.TextField(blank=True, null=True, verbose_name="Descrição Adicional")
    
        class Meta:
            verbose_name = "Cobrança de Mensalista"
            verbose_name_plural = "Cobranças de Mensalistas"
            ordering = ['-mes_referencia', '-data_geracao']
            unique_together = (('cliente_mensalista', 'mes_referencia'),)

        def __str__(self):
            return f"Mensalidade {self.mes_referencia} - {self.cliente_mensalista.usuario.username} - R${self.valor_devido:.2f} ({self.status})"

        def esta_vencida(self):
            return self.data_vencimento and self.data_vencimento < timezone.now().date() and self.status == 'pendente'

        def esta_paga(self):
            return self.status == 'pago'

        def calcular_saldo_pendente(self):
            return self.valor_devido - self.valor_pago
    
        def salvar_pagamento(self, valor_recebido):
            """
            Método para registrar um pagamento para esta cobrança de mensalista.
            """
            if self.esta_paga():
                return "Cobranca já paga."

            valor_recebido = Decimal(str(valor_recebido))
            if valor_recebido <= 0:
                return "Valor recebido deve ser positivo."

            saldo_anterior = self.calcular_saldo_pendente()

            if valor_recebido >= saldo_anterior:
                self.valor_pago += saldo_anterior
                self.status = 'pago'
                self.data_pagamento = timezone.now()
                self.save()
                return f"Cobrança {self.id} paga integralmente! Troco: R${valor_recebido - saldo_anterior:.2f}."
        
class CobrancaMensalista(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
    ]

    cliente_mensalista = models.ForeignKey(Mensalista, on_delete=models.CASCADE, verbose_name="Cliente Mensalista")
    
    data_geracao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Geração")
    data_vencimento = models.DateField(verbose_name="Data de Vencimento")
    mes_referencia = models.CharField(max_length=7, verbose_name="Mês de Referência (MM/AAAA)", help_text="Para cobranças mensais, ex: 05/2025")

    valor_devido = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Devido")
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name="Valor Pago")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente', verbose_name="Status")
    data_pagamento = models.DateTimeField(null=True, blank=True, verbose_name="Data do Pagamento")
    
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição Adicional")
    
    class Meta:
        verbose_name = "Cobrança de Mensalista"
        verbose_name_plural = "Cobranças de Mensalistas"
        ordering = ['-mes_referencia', '-data_geracao']
        unique_together = (('cliente_mensalista', 'mes_referencia'),)

    def __str__(self):
        return f"Mensalidade {self.mes_referencia} - {self.cliente_mensalista.usuario.username} - R${self.valor_devido:.2f} ({self.status})"

    def esta_vencida(self):
        return self.data_vencimento and self.data_vencimento < timezone.now().date() and self.status == 'pendente'

    def esta_paga(self):
        return self.status == 'pago'

    def calcular_saldo_pendente(self):
        return self.valor_devido - self.valor_pago
    
    def salvar_pagamento(self, valor_recebido):
        """
        Método para registrar um pagamento para esta cobrança de mensalista.
        """
        if self.esta_paga():
            return "Cobranca já paga."

        valor_recebido = Decimal(str(valor_recebido))
        if valor_recebido <= 0:
            return "Valor recebido deve ser positivo."

        saldo_anterior = self.calcular_saldo_pendente()

        if valor_recebido >= saldo_anterior:
            self.valor_pago += saldo_anterior
            self.status = 'pago'
            self.data_pagamento = timezone.now()
            self.save()
            return f"Cobrança {self.id} paga integralmente! Troco: R${valor_recebido - saldo_anterior:.2f}."