from django import forms

class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='E-mail'
    )