from django.db import models
from django.utils import timezone
from core.models import Usuario
from decimal import Decimal
import math

class Movimento(models.Model):
    placa_veiculo = models.CharField(max_length=8, verbose_name="Placa do Veículo")
    hora_entrada = models.DateTimeField(auto_now_add=True, verbose_name="Hora da Entrada")
    hora_saida = models.DateTimeField(null= True, blank= True, verbose_name="Hora da Saída")
    valor_total_calculado = models.DecimalField(max_digits=10, decimal_places=2, null= True, blank= True, verbose_name="Valor Total Calculado")
    
    registrado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, 
                                        related_name='movimentos_registrados', verbose_name="Registrado Por")

    class Meta:
        verbose_name = "Movimento de Estacionamento"
        verbose_name_plural = "Movimentos de Estacionamento"
        ordering = ['-hora_entrada']

    def __str__(self):
        return f"Movimento {self.placa_veiculo} - Entrada: {self.hora_entrada.strftime('%d/%m %H:%M')}"
    
    def calcular_tempo_estacionado(self):
        if self.hora_saida:
            return self.hora_saida - self.hora_entrada
        return None
    
    def calcular_total_estacionamento(self):
        tempo = self.calcular_tempo_estacionado()
        if tempo:
            tarifa = ConfiguracaoTarifa.objects.filter(ativa=True).first()
            if not tarifa:
                return Decimal('0.00')
            
            minutos_estacionados = tempo.total_seconds() / 60

            if minutos_estacionados <= 60:
                return tarifa.valor_inicial
            else:
                horas_completas_apos_primeira = (minutos_estacionados - 60) / 60
                horas_decimal = Decimal(horas_completas_apos_primeira).quantize(Decimal("0.01"))
                valor = tarifa.valor_inicial + (horas_decimal * tarifa.valor_hora_adicional)
                
                if tarifa.valor_diaria and minutos_estacionados > 24 * 60:
                     dias_completos = math.ceil(minutos_estacionados / (24 * 60))
                     valor_por_diaria = Decimal(str(dias_completos)) * tarifa.valor_diaria
                     if valor_por_diaria < valor:
                         valor = valor_por_diaria
                
                return valor.quantize(Decimal('0.01'))

class ConfiguracaoTarifa(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome da Tarifa")
    valor_inicial = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Inicial")
    valor_hora_adicional = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor das Horas Adicionais")
    valor_diaria = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Valor da diária")
    valor_mensal_avulso = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Valor Mensal Avulso")

    ativa = models.BooleanField(default=True, verbose_name= "Tarifa Ativa")

    class Meta:
        verbose_name = "Configuração de Tarifa"
        verbose_name_plural = "Configurações de Tarifas"

    def __str__(self):
        return self.nome

class PlanoMensal(models.Model):
    nome_plano= models.CharField(max_length=100, unique=True, verbose_name="Nome do Plano")
    valor_mensal= models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor da Mensalidade")
    descricao = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Plano Mensal"
        verbose_name_plural = "Planos Mensais"

    def __str__(self):
        return f"{self.nome_plano} (R${self.valor_mensal:.2f})"
    
class ClienteMensalista(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, verbose_name="Usuário")
    plano = models.ForeignKey(PlanoMensal, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Plano Mensal")
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    ativo = models.BooleanField(default=True, verbose_name="Ativo no Plano")
    email_para_cobranca = models.EmailField(blank=True, null=True, verbose_name="E-mail para Cobrança")

    class Meta:
        verbose_name = "Cliente Mensalista"
        verbose_name_plural = "Clientes Mensalistas" 

    def __str__(self):
        return f"{self.usuario.get_full_name() or self.usuario.username} ({'Ativo' if self.ativo else 'Inativo'})"

    def get_email_para_cobranca(self):
        return self.email_para_cobranca or self.usuario.email

class CobrancaDiarista(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
    ]

    movimento = models.OneToOneField(Movimento, on_delete=models.CASCADE, verbose_name="Movimento de Estacionamento")
    
    data_geracao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Geração")
    data_vencimento = models.DateField(verbose_name="Data de Vencimento")
    
    valor_devido = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Devido")
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name="Valor Pago")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente', verbose_name="Status")
    data_pagamento = models.DateTimeField(null=True, blank=True, verbose_name="Data do Pagamento")
    
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição Adicional")

    class Meta:
        verbose_name = "Cobrança de Diarista"
        verbose_name_plural = "Cobranças de Diaristas"
        ordering = ['-data_geracao']

    def __str__(self):
        return f"Cobranca Diarista {self.movimento.placa_veiculo} - R${self.valor_devido:.2f} ({self.status})"

    def esta_vencida(self):
        return self.data_vencimento and self.data_vencimento < timezone.now().date() and self.status == 'pendente'

    def esta_paga(self):
        return self.status == 'pago'

    def calcular_saldo_pendente(self):
        return self.valor_devido - self.valor_pago

    def salvar_pagamento(self, valor_recebido):
        """
        Método para registrar um pagamento para esta cobrança de diarista.
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

    cliente_mensalista = models.ForeignKey(ClienteMensalista, on_delete=models.CASCADE, verbose_name="Cliente Mensalista")
    
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