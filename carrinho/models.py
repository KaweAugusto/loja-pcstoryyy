from django.db import models
from django.conf import settings
from produto.models import Produto

class Carrinho(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carrinho', null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"Carrinho de {self.user.username}"
        return f"Carrinho da sessão {self.session_key}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.itens.all())

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} no carrinho"

    @property
    def subtotal(self):
        return self.produto.preco * self.quantidade