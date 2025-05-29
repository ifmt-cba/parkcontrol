from django.db import models
from django.utils import timezone
from core.models import usuario
from decimal import Decimal

class Movimento(models.Model):
    placa_veiculo = models.CharField(max_length=8, verbose_name="Placa do Veículo")
    hora_entrada = models.DateTimeField(default=timezone.now, verbose_name="Hora da Entrada")
    hora_saida = models.DateTimeField(null= True, blank= True, verbose_name="Hora da Saída")
    valor_total_calculado = models.DecimalField(max_digits=10, decimal_places=2, null= True, blank= True, verbose_name="Valor Total Calculado")

    class Meta:
        verbose_name = "Movimento de Estacionamento"
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

                return valor.quantize(Decimal('0.01'))

class ConfiguracaoTarifa(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome da Tarifa")
    valor_inicial = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Inicial")
    valor_hora_adicional = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor das Horas Adicionais ")
    valor_diaria = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor da diária")
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
    usuario = models.OneToOneField(usuario, on_delete=models.CASCADE, verbose_name="Usuário")
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

class Cobranca(models.Model):
        
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
    ]

    TIPO_COBRANCA_CHOICES = [
        ('por_periodo', 'Por Período'),
        ('mensal', 'Mensalidade'),
        ('avulsa', 'Avulsa'),
    ]

    movimento = models.OneToOneField(Movimento, on_delete=models.SET_NULL, null=True, blank=True, help_text="Movimento de estacionamento associado a esta cobrança (para diaristas)", verbose_name="Movimento Avulso")
    cliente_mensalista = models.ForeignKey(ClienteMensalista, on_delete=models.SET_NULL, null=True, blank=True, help_text="Cliente Mensalista associado à cobrança", verbose_name="Cliente Mensalista")
    
    data_geracao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Geração")
    data_vencimento = models.DateField(verbose_name="Data de Vencimento")
    
    mes_referencia = models.CharField(max_length=7, null=True, blank=True, verbose_name="Mês de Referência (MM/AAAA)",
                                      help_text="Para cobranças mensais, ex: 05/2025")
    
    valor_devido = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Devido")
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name="Valor Pago")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente', verbose_name="Status")
    data_pagamento = models.DateTimeField(null=True, blank=True, verbose_name="Data do Pagamento")
    tipo_cobranca = models.CharField(max_length=50, choices=TIPO_COBRANCA_CHOICES, verbose_name="Tipo de Cobrança")
    
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição Adicional")

    class Meta:
        verbose_name = "Cobrança"
        verbose_name_plural = "Cobranças"
        ordering = ['-data_geracao']

    def __str__(self):
        if self.tipo_cobranca == 'mensal' and self.cliente_mensalista:
            return f"Mensalidade {self.mes_referencia} - {self.cliente_mensalista.usuario.username} - R${self.valor_devido:.2f} ({self.status})"
        elif self.movimento:
            return f"Cobranca Avulsa {self.movimento.placa_veiculo} - R${self.valor_devido:.2f} ({self.status})"
        return f"Cobranca #{self.id} - R${self.valor_devido:.2f} ({self.status})"

    def esta_vencida(self):
        return self.data_vencimento and self.data_vencimento < timezone.now().date() and self.status == 'pendente'

    def esta_paga(self):
        return self.status == 'pago'

    def calcular_saldo_pendente(self):
        return self.valor_devido - self.valor_pago