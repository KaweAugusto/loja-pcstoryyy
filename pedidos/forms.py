from django import forms
from django.forms import inlineformset_factory
from .models import Pedido, ItemPedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        # O campo 'cliente' será preenchido automaticamente pela view
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

# Cria um "conjunto de formulários" para os itens do pedido
ItemPedidoFormSet = inlineformset_factory(
    Pedido,  # Modelo pai
    ItemPedido,  # Modelo filho
    fields=('produto', 'quantidade', 'preco'),  # Campos a serem exibidos para cada item
    extra=1,  # Começa com 1 formulário de item extra
    can_delete=True,  # Permite deletar itens
    widgets={
        'produto': forms.Select(attrs={'class': 'form-control'}),
        'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        'preco': forms.NumberInput(attrs={'class': 'form-control'}),
    }
)