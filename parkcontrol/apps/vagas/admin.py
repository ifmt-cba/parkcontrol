from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Vaga, EntradaVeiculo, SaidaVeiculo, SolicitacaoManutencao


@admin.register(Vaga)
class VagaAdmin(SimpleHistoryAdmin):
    list_display = ('numero', 'status')
    list_filter = ('status',)
    search_fields = ('numero',)
    ordering = ('numero',)


@admin.register(EntradaVeiculo)
class EntradaVeiculoAdmin(SimpleHistoryAdmin):
    list_display = ('nome', 'placa', 'tipo_cliente', 'horario_entrada', 'vaga')
    list_filter = ('tipo_cliente', 'vaga')
    search_fields = ('nome', 'placa')
    ordering = ('-horario_entrada',)


@admin.register(SaidaVeiculo)
class SaidaVeiculoAdmin(SimpleHistoryAdmin):
    list_display = ('placa', 'tipo_cliente', 'tempo_permanencia', 'horario_saida', 'valor_total')
    list_filter = ('tipo_cliente',)
    search_fields = ('placa',)
    ordering = ('-horario_saida',)


@admin.register(SolicitacaoManutencao)
class SolicitacaoManutencaoAdmin(SimpleHistoryAdmin):
    list_display = ('numero_vaga', 'descricao', 'data_solicitacao', 'solicitante', 'resolvido')
    list_filter = ('resolvido', 'data_solicitacao')
    search_fields = ('numero_vaga__numero', 'descricao', 'solicitante__username')
    ordering = ('-data_solicitacao',)
