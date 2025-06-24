from simple_history.models import HistoricalRecords
from django.db import models
from django.core.validators import RegexValidator
from apps.planos.models import Planos

class Mensalista(models.Model):
    nome = models.CharField(max_length=100)
    
    telefone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                r'^\(?\d{2}\)?[-.\s]?\d{4,5}[-.\s]?\d{4}$',
                'Telefone no formato inválido (ex: (65) 99999-9999)'
            )
        ]
    )

    email = models.EmailField(max_length=100)
    plano = models.ForeignKey(
        Planos,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'tipo_plano': 'Mensalista'}, 
        related_name="mensalistas"
    )

    placa = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                r'^[A-Z]{3}[0-9][A-Z][0-9]{2}$',
                'Placa no formato inválido (ex: ABC1D23 - padrão Mercosul)'
            )
        ]
    )
   
    ativo = models.BooleanField(default=True)
    historico = HistoricalRecords()  # Adiciona histórico de alterações
    def __str__(self):
        return f'Nome: {self.nome} - Placa: {self.placa} - Plano: {self.plano} - Telefone: {self.telefone} - Email: {self.email} - Status: {"Ativo" if self.ativo else "Inativo"}'

class Diarista(models.Model):
    nome = models.CharField(max_length=100)
    
    telefone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                r'^\(?\d{2}\)?[-.\s]?\d{4,5}[-.\s]?\d{4}$',
                'Telefone no formato inválido (ex: (65) 99999-9999)'
            )
        ]
    )
    plano = models.ForeignKey(
        Planos,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'tipo_plano': 'Diarista'},
        related_name="diaristas"
    )
    placa = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                r'^[A-Z]{3}[0-9][A-Z][0-9]{2}$',
                'Placa no formato inválido (ex: ABC1D23 - padrão Mercosul)'
            )
        ]
    )

    ativo = models.BooleanField(default=True)
    historico = HistoricalRecords()
    def __str__(self):
        return f'Nome: {self.nome} - Placa: {self.placa} - Telefone: {self.telefone} - Status: {"Ativo" if self.ativo else "Inativo"}'