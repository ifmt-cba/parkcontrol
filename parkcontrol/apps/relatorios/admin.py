from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import RelatorioFinanceiro


@admin.register(RelatorioFinanceiro)
class RelatorioFinanceiroAdmin(SimpleHistoryAdmin):
    list_display = (
        'nome',
        'criado_por',
        'data_inicio',
        'data_fim',
        'status',
        'total_emitido',
        'total_pago',
        'total_inadimplente',
        'data_criacao',
    )
    list_filter = ('status', 'data_criacao', 'data_inicio', 'data_fim')
    search_fields = ('nome', 'criado_por__username')
    ordering = ('-data_criacao',)
    date_hierarchy = 'data_criacao'
    readonly_fields = ('data_criacao', 'editado_em')

    fieldsets = (
        ('Informações do Relatório', {
            'fields': ('nome', 'criado_por', 'status', 'data_inicio', 'data_fim', 'arquivo_pdf')
        }),
        ('Valores Financeiros', {
            'fields': ('total_emitido', 'total_pago', 'total_inadimplente')
        }),
        ('Datas', {
            'fields': ('data_criacao', 'editado_em')
        }),
    )
