from django import forms
from .models import Mensalista, Diarista

class MensalistaForm(forms.ModelForm):
    class Meta:
        model = Mensalista
        fields = ['nome', 'email', 'telefone', 'placa', 'plano']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'plano': forms.Select(attrs={'class': 'form-control'}),
            'placa': forms.TextInput(attrs={'class': 'form-control'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class DiaristaForm(forms.ModelForm):
    class Meta:
        model = Diarista
        fields = ['nome', 'telefone', 'placa']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'placa': forms.TextInput(attrs={'class': 'form-control'}),
        }
