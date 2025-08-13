from django.contrib import admin
from .models import Pedido, ItemPedido

class ItemInline(admin.TabularInline):
    model = ItemPedido
    extra = 1

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'criado_em', 'total')
    inlines = [ItemInline]
