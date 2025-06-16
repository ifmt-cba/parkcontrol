from django.db import models

# Create your models here.
class Planos(models.Model):

    TIPO_PLANO_CHOICES = [
        ('Mensalista', 'Mensalista'),
        ('Diarista', 'Diarista'),
    ]

    TIPO_MENSAL_CHOICES = [
        ('Mensal', 'Mensal'),
        ('Anual','Anual')
    ]
    
    STATUS_CHOICES = [
        ('Ativo', 'Ativo'),
        ('Inativo', 'Inativo'),
    ]

    nome = models.CharField( max_length=50, blank=False, null=False)
    validade = models.PositiveIntegerField(blank=False, null=False)
    descricao = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_alteracao = models.DateTimeField(auto_now=True)
    tipo_plano = models.CharField(max_length=20, choices=TIPO_PLANO_CHOICES, blank=False, null=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True,default='Ativo')

    # Informações somente do plano Diarista
    valor_diaria = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Informações somente do plano Mensalista
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tipo_mensal  = models.CharField(max_length=20, choices=TIPO_MENSAL_CHOICES, blank=True, null=True)

    def __str__(self):
     return self.nome
