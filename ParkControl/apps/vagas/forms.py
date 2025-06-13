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
        fields = ['placa', 'nome', 'vaga']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra apenas vagas livres
        self.fields['vaga'].queryset = Vaga.objects.filter(status='Livre')

class SaidaVeiculoForm(forms.ModelForm):
    class Meta:
        model = SaidaVeiculo
        fields = ['placa']

class SolicitacaoManutencaoForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoManutencao
        fields = ['numero_vaga', 'descricao']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['numero_vaga'].widget.attrs.update({'class': 'form-control'})
        self.fields['descricao'].widget.attrs.update({'class': 'form-control'})