# apps/pagamentos/forms.py
from django import forms

from apps.clientes.models import Mensalista
from apps.planos.models import Planos

from .models import CobrancaDiarista, CobrancaMensalista 

from django.core.exceptions import ValidationError
import re
from decimal import Decimal
from django.contrib import messages

class GerarCobrancaMensalForm(forms.Form):
    cliente_mensalista = forms.ModelChoiceField(
        queryset=Mensalista.objects.filter(ativo=True),
        label="Cliente Mensalista",
        empty_label="Selecione um cliente mensalista",
        error_messages={'required': 'Selecione um cliente mensalista para gerar a cobrança.'}
    )

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
        cliente_mensalista_obj = cleaned_data.get('cliente_mensalista')
        mes_referencia_str = cleaned_data.get('mes_referencia')
        valor_digitado = cleaned_data.get('valor_devido')

        from apps.planos.models import Planos as PlanosApp 

        if cliente_mensalista_obj and cliente_mensalista_obj.plano:
            try:
                plano_do_cliente = PlanosApp.objects.get(
                    nome=cliente_mensalista_obj.plano, 
                    tipo_plano='Mensalista', 
                    status='Ativo' 
                )
                valor_plano_esperado = plano_do_cliente.valor 
                
                if valor_digitado and valor_digitado != valor_plano_esperado:
                    messages.warning(self.request, f"Atenção: O valor informado (R$ {valor_digitado:.2f}) é diferente do valor do plano (R$ {valor_plano_esperado:.2f}).")
            except PlanosApp.DoesNotExist:
                messages.warning(self.request, f"Atenção: O plano '{cliente_mensalista_obj.plano}' do cliente não foi encontrado ou está inativo. Preencha o valor manualmente.")
            except Exception as e:
                 messages.error(self.request, "Erro ao verificar o plano: %s" % str(e))
        else:
            messages.warning(self.request, "Atenção: Cliente não possui plano definido ou válido. Preencha o valor manualmente.")

        if cliente_mensalista_obj and mes_referencia_str:
            if CobrancaMensalista.objects.filter(
                cliente_mensalista=cliente_mensalista_obj,
                mes_referencia=mes_referencia_str,
            ).exists():
                raise ValidationError(
                    f"Já existe uma cobrança mensal para {cliente_mensalista_obj.nome} referente ao mês {mes_referencia_str}."
                )
        
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

class CobrancaDiaristaStatusForm(forms.ModelForm):
    class Meta:
        model = CobrancaDiarista
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