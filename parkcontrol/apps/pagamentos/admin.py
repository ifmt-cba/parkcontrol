from django.contrib import admin
from .models import EntradaVeiculo, Movimento, ConfiguracaoTarifa, CobrancaDiarista, CobrancaMensalista

@admin.register(EntradaVeiculo)
class EntradaVeiculoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'placa', 'nome', 'horario_entrada', 'tipo_cliente', 
        'cliente_diarista', 'cliente_mensalista'
    )
    list_filter = ('tipo_cliente', 'horario_entrada')
    search_fields = ('placa', 'nome')
    raw_id_fields = ('cliente_diarista', 'cliente_mensalista')
    readonly_fields = ('horario_entrada',)

class MovimentoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'entrada_placa', 'entrada_tipo_cliente', 'hora_entrada_real', 
        'hora_saida', 'valor_total_calculado'
    )
    list_filter = ('hora_saida', 'valor_total_calculado')
    search_fields = ('entrada__placa',) 
    raw_id_fields = ('entrada',)
    readonly_fields = ('hora_entrada_real',) 

    @admin.display(description='Placa')
    def entrada_placa(self, obj):
        return obj.entrada.placa if obj.entrada else 'N/A'

    @admin.display(description='Tipo Cliente')
    def entrada_tipo_cliente(self, obj):
        return obj.entrada.get_tipo_cliente_display() if obj.entrada else 'N/A'
    
    @admin.display(description='Hora Entrada')
    def hora_entrada_real(self, obj):
        return obj.entrada.horario_entrada if obj.entrada else 'N/A'

class ConfiguracaoTarifaAdmin(admin.ModelAdmin):
    list_display = (
        'nome', 'valor_inicial', 'valor_hora_adicional', 
        'valor_diaria', 'valor_mensal_avulso', 'ativa'
    )
    list_filter = ('ativa',)
    search_fields = ('nome',)

class CobrancaDiaristaAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'movimento_placa', 'data_geracao', 'data_vencimento', 
        'valor_devido', 'valor_pago', 'status', 'data_pagamento'
    )
    list_filter = ('status', 'data_geracao', 'data_vencimento')
    search_fields = ('movimento__placa_veiculo',)
    raw_id_fields = ('movimento',) 
    
    @admin.display(description='Placa')
    def movimento_placa(self, obj):
        return obj.movimento.placa_veiculo if obj.movimento else 'N/A'

class CobrancaMensalistaAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'cliente_mensalista_nome', 'mes_referencia', 'data_geracao', 
        'data_vencimento', 'valor_devido', 'valor_pago', 'status', 'data_pagamento'
    )
    list_filter = ('status', 'mes_referencia', 'data_geracao', 'data_vencimento')
    search_fields = ('cliente_mensalista__nome', 'cliente_mensalista__placa', 'mes_referencia')
    raw_id_fields = ('cliente_mensalista',)
    
    @admin.display(description='Cliente Mensalista')
    def cliente_mensalista_nome(self, obj):
        return obj.cliente_mensalista.nome if obj.cliente_mensalista else 'N/A'