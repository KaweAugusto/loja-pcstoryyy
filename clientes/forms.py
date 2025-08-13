# clientes/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Cliente


# -----------------------------------------------------------------------------
# FORMULÁRIO PARA CADASTRO DE NOVOS CLIENTES (PÚBLICO)
# -----------------------------------------------------------------------------
class ClienteCreationForm(UserCreationForm):
    # Campos customizados que serão adicionados ao formulário de criação
    nome_completo = forms.CharField(max_length=150, required=True, label='Nome Completo')
    endereco = forms.CharField(max_length=255, required=True, label='Endereço')
    email = forms.EmailField(required=True, label='E-mail')

    class Meta(UserCreationForm.Meta):
        model = User
        # O UserCreationForm já inclui os campos de senha (password e password2)
        # Nós apenas informamos que o campo 'email' também fará parte do formulário do User.
        fields = ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Usa o email como username
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['nome_completo']

        if commit:
            user.save()
            # Cria o objeto Cliente vinculado
            Cliente.objects.create(
                user=user,
                nome=self.cleaned_data['nome_completo'],
                email=self.cleaned_data['email'],
                endereco=self.cleaned_data['endereco']
            )
        return user


# -----------------------------------------------------------------------------
# FORMULÁRIO PARA LOGIN DE CLIENTES E ADMIN
# -----------------------------------------------------------------------------
class LoginForm(forms.Form):
    """
    Formulário de login que aceita tanto o nome de usuário quanto o e-mail.
    """
    username = forms.CharField(max_length=150, required=True, label='E-mail ou Usuário')
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Senha')


# -----------------------------------------------------------------------------
# FORMULÁRIO PARA CRUD DE CLIENTES (ADMIN)
# -----------------------------------------------------------------------------
class ClienteForm(forms.ModelForm):
    """
    Este formulário é ideal para a área administrativa (ou área restrita),
    onde você, como admin, pode criar ou editar um cliente existente.
    """

    class Meta:
        model = Cliente
        fields = ['user', 'nome', 'telefone', 'endereco']