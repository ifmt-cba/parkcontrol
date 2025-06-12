from django import forms
from .models import Planos

class PlanoMensalForm(forms.ModelForm):
    class Meta:
        model = Planos
        fields = ['nome', 'validade', 'descricao', 'status', 'valor', 'tipo_mensal']
        
class PlanoDiarioForm(forms.ModelForm):
    class Meta:
        model = Planos
        fields = ['nome', 'validade', 'descricao', 'status', 'valor_diaria']
