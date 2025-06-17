# apps/pagamentos/forms.py
from django import forms

from apps.clientes.models import Mensalista
from apps.planos.models import Planos

from .models import CobrancaMensalista 

from django.core.exceptions import ValidationError
import re
from decimal import Decimal

class GerarCobrancaMensalForm(forms.Form):

    mes_referencia = forms.CharField(
        max_length=7,
        label="Mês de Referência (MM/AAAA)",
        help_text="Ex: 05/2025",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/AAAA'})
    )
    
    data_vencimento = forms.DateField(
        label="Data de Vencimento",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        error_messages={'required': 'A data de vencimento é obrigatória.'}
    )
    
    valor_devido = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Valor da Cobrança",
        min_value=Decimal('0.01'),
        localize=True,
        error_messages={'required': 'O valor da cobrança é obrigatório.'}
    )

    def clean_mes_referencia(self):
        mes_referencia = self.cleaned_data['mes_referencia']
        if not re.match(r'^(0[1-9]|1[0-2])/\d{4}$', mes_referencia):
            raise ValidationError("Formato de mês/ano inválido. Use MM/AAAA.")
        return mes_referencia

    def clean(self):
        cleaned_data = super().clean()
        mes_referencia_str = cleaned_data.get('mes_referencia')
        valor_digitado = cleaned_data.get('valor_devido')

        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

class CobrancaMensalistaStatusForm(forms.ModelForm):
    class Meta:
        model = CobrancaMensalista
        fields = ['status', 'valor_pago']
    
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        valor_pago = cleaned_data.get('valor_pago')

        if status == 'pago' and self.instance.valor_devido > 0:
            if valor_pago < self.instance.valor_devido:
                raise ValidationError(
                    "Para marcar como 'Pago', o valor pago deve ser igual ou maior que o valor devido."
                )
        return cleaned_data