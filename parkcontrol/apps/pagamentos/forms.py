from django import forms
from .models import ClienteMensalista # Importe o modelo ClienteMensalista se ainda não o fez

class GerarCobrancaMensalForm(forms.Form):
    cliente_mensalista = forms.ModelChoiceField(
        queryset=ClienteMensalista.objects.all(),
        label="Cliente Mensalista",
        widget=forms.Select(attrs={'class': 'form-select'}) 
    )
    mes_referencia = forms.CharField(
        label="Mês de Referência (Ex: AAAA-MM)", # Ex: 2025-06
        max_length=7, # Para o formato AAAA-MM
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'AAAA-MM'})
    )
    data_vencimento = forms.DateField(
        label="Data de Vencimento",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    valor_devido = forms.DecimalField(
        label="Valor Devido (R$)",
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )

    # Você pode adicionar um método clean_mes_referencia para validar o formato, se desejar
    def clean_mes_referencia(self):
        mes = self.cleaned_data.get('mes_referencia')
        # Adicione aqui validações para o formato AAAA-MM, se necessário
        # Exemplo simples (pode ser mais robusto):
        if mes and (len(mes) != 7 or mes[4] != '-'):
            raise forms.ValidationError("Formato inválido. Use AAAA-MM (ex: 2025-06).")
        return mes
    
class CobrancaDiaristaStatusForm(forms.Form):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, label="Novo Status", widget=forms.Select(attrs={'class': 'form-select'}))
        # Adicione outros campos se necessário, como data_pagamento, valor_pago, etc.

class CobrancaMensalistaStatusForm(forms.Form):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('vencido', 'Vencido'),
        ('cancelado', 'Cancelado'),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, label="Novo Status", widget=forms.Select(attrs={'class': 'form-select'}))