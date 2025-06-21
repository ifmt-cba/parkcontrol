from django import forms
from .models import RelatorioFinanceiro

class FormularioRelatorioFinanceiro(forms.ModelForm):
    class Meta:
        model = RelatorioFinanceiro
        exclude = ['arquivo_pdf', 'criado_por', 'data_criacao', 'editado_em', 'total_emitido', 'total_pago', 'total_inadimplente']
