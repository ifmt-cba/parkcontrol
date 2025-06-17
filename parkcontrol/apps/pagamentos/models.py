from django.utils import timezone
from django.db import models

# Create your models here.
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