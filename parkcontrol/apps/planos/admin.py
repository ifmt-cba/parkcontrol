from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Planos


@admin.register(Planos)
class PlanosAdmin(SimpleHistoryAdmin):
    list_display = ('nome', 'tipo_plano', 'tipo_mensal', 'valor', 'valor_diaria', 'status', 'validade', 'data_criacao')
    list_filter = ('tipo_plano', 'tipo_mensal', 'status')
    search_fields = ('nome',)
    ordering = ('-data_criacao',)
