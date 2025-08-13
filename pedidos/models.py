# pedidos/models.py
from django.db import models
from clientes.models import Cliente
from produto.models import Produto # <--- ESTA LINHA FOI CORRIGIDA
from decimal import Decimal


class Pedido(models.Model):
    STATUS_CHOICES = [
        ('ABERTO', 'Aberto'),
        ('ENVIADO', 'Enviado'),
        ('CANCELADO', 'Cancelado'),
    ]

    STATUS_CANCELAMENTO_CHOICES = [
        ('nenhum', 'Nenhum'),
        ('solicitado', 'Aguardando confirmação'),
        ('cancelado', 'Cancelado'),
        ('recusado', 'Recusado'),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='pedidos'
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ABERTO')

    # Controle de cancelamento
    status_cancelamento = models.CharField(
        max_length=20,
        choices=STATUS_CANCELAMENTO_CHOICES,
        default='nenhum'
    )
    motivo_cancelamento = models.TextField(blank=True, null=True)

    # Total salvo no banco
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calcular_total(self):
        """Recalcula o valor total e salva no banco."""
        self.total = sum(item.subtotal() for item in self.itens.all())
        self.save(update_fields=['total'])

    def __str__(self):
        return f'Pedido #{self.id} - {self.cliente.nome}'


class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        related_name='itens',
        on_delete=models.CASCADE
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT
    )
    quantidade = models.PositiveIntegerField(default=1)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        """Calcula o subtotal do item."""
        return Decimal(self.preco) * self.quantidade

    def save(self, *args, **kwargs):
        """Atualiza o total do pedido ao salvar item."""
        super().save(*args, **kwargs)
        self.pedido.calcular_total()

    def delete(self, *args, **kwargs):
        """Atualiza o total do pedido ao deletar item."""
        super().delete(*args, **kwargs)
        self.pedido.calcular_total()

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome} (Pedido #{self.pedido.id})'