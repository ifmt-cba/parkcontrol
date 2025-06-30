from django.db import models
from django.contrib.auth.models import AbstractUser
from simple_history.models import HistoricalRecords


class Usuario(AbstractUser):
    perfil_acesso = models.CharField(max_length=20, choices=[
        ('Administrador', 'Administrador'),
        ('Frentista', 'Frentista'),
        ('Contador', 'Contador')
    ])

    historico = HistoricalRecords()  # Adiciona histórico de alterações
