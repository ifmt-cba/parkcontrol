from django import forms
from apps.clientes.models import Mensalista
from apps.planos.models import Planos
from .models import CobrancaMensalista 
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import date 

class GerarCobrancaMensalForm(forms.Form):
    mes = forms.ChoiceField(
        label="Mês de Referência",
        choices=[(i, f'{i:02d}') for i in range(1, 13)], 
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    ano = forms.ChoiceField(
        label="Ano de Referência",
        choices=[(y, str(y)) for y in range(date.today().year - 5, date.today().year + 5)], 
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    data_vencimento = forms.DateField(
        label="Data de Vencimento",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        error_messages={'required': 'A data de vencimento é obrigatória.'}
    )

    def clean(self):
        cleaned_data = super().clean()
        mes = cleaned_data.get('mes')
        ano = cleaned_data.get('ano')
        
        if mes and ano:
            cleaned_data['mes_referencia_str'] = f"{int(mes):02d}/{ano}" 
        
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        if not self.is_bound and self.initial:
            today = date.today()
            self.initial.setdefault('mes', today.month)
            self.initial.setdefault('ano', today.year)

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