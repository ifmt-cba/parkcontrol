from django.db import models

# Create your models here.
from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from django.db import models
from django.core.validators import RegexValidator


class Vaga(models.Model):
    numero = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=[('Livre', 'Livre'), ('Manutenção', 'Manutenção'), ('Ocupada', 'Ocupada')], default='Livre')

    def __str__(self):
        return f'Vaga {self.numero} - {self.status}'
    
class EntradaVeiculo(models.Model):
    TIPO_VEICULO_CHOICES = [
        ('Carro', 'Carro'),
        ('Moto', 'Moto'),
    ]

    nome = models.CharField(max_length=100)
    tipo_cliente = models.CharField(max_length=12) 
    placa = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                r'^[A-Z]{3}[0-9][A-Z][0-9]{2}$',
                'Placa no formato inválido (ex: ABC1D23 - padrão Mercosul)'
            )
        ]
    )  
    
    tipo_veiculo = models.CharField(max_length=10, choices=TIPO_VEICULO_CHOICES)
    horario_entrada = models.DateTimeField(default=timezone.now)

    vaga = models.ForeignKey(
    'Vaga',
    on_delete=models.PROTECT,
    related_name='entradas',
    null=True,
    blank=True
    )

    def __str__(self):
        return f'Nome: {self.nome} - Placa: {self.placa} - Horario Entrada:{self.horario_entrada}'

class SaidaVeiculo(models.Model):

    entrada = models.ForeignKey(
        'EntradaVeiculo',
        on_delete=models.CASCADE,
        related_name='saidas'
    )

    placa = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                r'^[A-Z]{3}[0-9][A-Z][0-9]{2}$',
                'Placa no formato inválido (ex: ABC1D23 - padrão Mercosul)'
            )
        ]
    )  
    tipo_veiculo = models.CharField(max_length=10)
    tipo_cliente = models.CharField(max_length=12)
    tempo_permanencia = models.DurationField(null=True, blank=True)
    horario_saida = models.DateTimeField(default=timezone.now)
    valor_total = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, default=0) 

    def __str__(self):
        return f'Placa: {self.placa} - Tempo Permanencia: {self.tempo_permanencia} - R${self.valor_total}'

def listar_vagas(request):
    vagas = Vaga.objects.all()
    return render(request, 'vagas/listar_vagas.html', {'vagas': vagas})

class SolicitacaoManutencao(models.Model):
    numero_vaga = models.CharField(max_length=10)
    descricao = models.TextField()
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    resolvido = models.BooleanField(default=False)

    def __str__(self):
        return f"Manutenção vaga {self.numero_vaga} - {'Resolvido' if self.resolvido else 'Pendente'}"