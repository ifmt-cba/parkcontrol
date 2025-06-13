from django.contrib import admin
from .models import  EntradaVeiculo, SaidaVeiculo, Vaga

admin.site.register(EntradaVeiculo)
admin.site.register(SaidaVeiculo)
admin.site.register(Vaga)

class SolicitacaoManutencaoAdmin(admin.ModelAdmin):
    list_display = ('numero_vaga', 'data_solicitacao', 'solicitante', 'resolvido')
    list_filter = ('resolvido',)

# Register your models here.
