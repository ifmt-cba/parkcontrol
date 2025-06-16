from django.db import models
from django.core.validators import RegexValidator

from ParkControl.apps.planos.models import Planos

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
<<<<<<< Updated upstream
    plano = models.ForeignKey(Planos, on_delete=models.PROTECT, related_name='mensalistas')
    
=======
    plano = models.ForeignKey(Planos, on_delete=models.SET_NULL, null=True, limit_choices_to={'tipo': 'Mensalista'}, related_name="mensalistas")

>>>>>>> Stashed changes
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
    plano = models.ForeignKey(Planos, on_delete=models.SET_NULL, null=True, limit_choices_to={'tipo': 'Diarista'}, related_name="diaristas")
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f'Nome: {self.nome} - Placa: {self.placa} - Telefone: {self.telefone} - Status: {"Ativo" if self.ativo else "Inativo"}'