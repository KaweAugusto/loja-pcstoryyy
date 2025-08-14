from django.db import models
from clientes.models import Cliente
from produto.models import Produto
from decimal import Decimal

class Pedido(models.Model):
    # Status mais completos para um fluxo de e-commerce
    STATUS_CHOICES = [
        ('AGUARDANDO_PAGAMENTO', 'Aguardando Pagamento'),
        ('CANCELAMENTO_SOLICITADO', 'Cancelamento Solicitado'),
        ('PROCESSANDO', 'Processando'),
        ('ENVIADO', 'Enviado'),
        ('ENTREGUE', 'Entregue'),
        ('CANCELADO', 'Cancelado'),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='pedidos'
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default='AGUARDANDO_PAGAMENTO'
    )

    class Meta:
        ordering = ['-criado_em'] # Mostra os pedidos mais recentes primeiro

    def __str__(self):
        return f'Pedido #{self.id} - {self.cliente.nome}'


class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        related_name='itens',
        on_delete=models.CASCADE # Se o pedido for deletado, os itens também são
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT # Impede que um produto em um pedido seja deletado
    )
    quantidade = models.PositiveIntegerField(default=1)
    preco = models.DecimalField(max_digits=10, decimal_places=2) # Preço no momento da compra

    @property
    def subtotal(self):
        """Calcula o subtotal do item."""
        return self.preco * self.quantidade

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome}'