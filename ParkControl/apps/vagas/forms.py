from django import forms
from .models import EntradaVeiculo, SaidaVeiculo, Vaga, SolicitacaoManutencao
class EntradaVeiculoForm(forms.ModelForm):
    vaga = forms.ModelChoiceField(
        queryset=Vaga.objects.filter(status='Livre'),
        label='Vaga'
    )
    nome = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control w-100'}))
    
    class Meta:
        model = EntradaVeiculo
        fields = ['placa', 'nome', 'vaga', 'tipo_cliente']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra apenas vagas livres
        self.fields['vaga'].queryset = Vaga.objects.filter(status='Livre')

class SaidaVeiculoForm(forms.Form):
    placa = forms.CharField(
        max_length=10,
        label='Placa',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

class SolicitacaoManutencaoForm(forms.ModelForm):
    numero_vaga = forms.ModelChoiceField(
        queryset=Vaga.objects.exclude(status='Ocupada'),
        label='Nº da Vaga',
        empty_label="Selecione uma vaga disponível"
    )

    class Meta:
        model = SolicitacaoManutencao
        fields = ['numero_vaga', 'descricao']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Refiltra novamente por segurança
        self.fields['numero_vaga'].queryset = Vaga.objects.exclude(status='Ocupada')
        self.fields['numero_vaga'].widget.attrs.update({'class': 'form-control'})
        self.fields['descricao'].widget.attrs.update({'class': 'form-control'})
