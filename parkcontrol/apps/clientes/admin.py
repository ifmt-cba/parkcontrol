from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Mensalista, Diarista


@admin.register(Mensalista)
class MensalistaAdmin(SimpleHistoryAdmin):
    list_display = ('nome', 'telefone', 'email', 'plano', 'placa', 'ativo')
    list_filter = ('ativo', 'plano')
    search_fields = ('nome', 'telefone', 'email', 'placa')
    ordering = ('nome',)
    list_per_page = 25


@admin.register(Diarista)
class DiaristaAdmin(SimpleHistoryAdmin):
    list_display = ('nome', 'telefone', 'plano', 'placa', 'ativo')
    list_filter = ('ativo', 'plano')
    search_fields = ('nome', 'telefone', 'placa')
    ordering = ('nome',)
    list_per_page = 25