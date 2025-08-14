from django import forms
from django.contrib.auth.models import User
from .models import Cliente

# -----------------------------------------------------------------------
# Formulários para a página "Minha Conta", onde o usuário edita os próprios dados.
# -----------------------------------------------------------------------

class UserEditForm(forms.ModelForm):
    """
    Formulário para o usuário editar suas próprias informações básicas.
    """
    class Meta:
        model = User
        # Campos que o usuário pode editar em sua conta
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail de Acesso'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu primeiro nome'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu sobrenome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}),
        }


class ClienteForm(forms.ModelForm):
    """
    Formulário para o usuário editar os dados do seu perfil de cliente.
    """
    class Meta:
        model = Cliente
        # Campos que o usuário pode editar em seu perfil
        fields = ['telefone', 'endereco']
        labels = {
            'telefone': 'Telefone para Contato',
            'endereco': 'Endereço Completo (para entregas)'
        }
        widgets = {
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(XX) XXXXX-XXXX'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ex: Rua das Flores, 123, Bairro, Cidade - UF, CEP'}),
        }