from django.contrib import admin
from .models import Mensalista, Diarista

@admin.register(Mensalista)
class MensalistaAdmin(admin.ModelAdmin):
    list_display = (
        'nome', 
        'placa', 
        'plano',
        'ativo', 
        'telefone', 
        'email'
    )

    list_filter = ('ativo', 'plano')
    search_fields = ('nome', 'placa', 'telefone', 'email', 'plano')
    list_editable = ('ativo', 'plano')

@admin.register(Diarista)
class DiaristaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'placa', 'ativo', 'telefone')
    list_filter = ('ativo',)
    search_fields = ('nome', 'placa', 'telefone')
    list_editable = ('ativo',)