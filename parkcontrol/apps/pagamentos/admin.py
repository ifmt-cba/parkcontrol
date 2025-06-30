from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from apps.pagamentos.models import CobrancaDiaria, CobrancaMensalista


@admin.register(CobrancaDiaria)
class CobrancaDiariaAdmin(SimpleHistoryAdmin):
    list_display = ('placa', 'nome', 'data', 'valor_total', 'status')
    search_fields = ('placa', 'nome')
    list_filter = ('status', 'data')
    ordering = ('-data',)


@admin.register(CobrancaMensalista)
class CobrancaMensalistaAdmin(SimpleHistoryAdmin):
    list_display = ('cliente_mensalista', 'mes_referencia', 'valor_devido', 'valor_pago', 'status', 'data_vencimento')
    search_fields = ('cliente_mensalista__nome', 'cliente_mensalista__usuario__username', 'mes_referencia')
    list_filter = ('status', 'mes_referencia')
    ordering = ('-mes_referencia', '-data_vencimento')
