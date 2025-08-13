# produto/admin.py
from django.contrib import admin
from .models import Produto, Categoria
from django.utils.html import format_html  # Para exibir HTML no admin

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco', 'estoque', 'preview_imagem')  # Mostra a imagem
    search_fields = ('nome',)  # Campo de busca
    list_filter = ('categoria',)  # Filtro lateral por categoria
    list_editable = ('preco', 'estoque')  # Editar preço e estoque direto na lista
    ordering = ('nome',)  # Ordenação padrão

    def preview_imagem(self, obj):
        """Exibe uma miniatura da imagem no admin"""
        if obj.imagem:
            return format_html('<img src="{}" width="50" style="border-radius: 5px;" />', obj.imagem.url)
        return "—"
    preview_imagem.short_description = "Imagem"


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)  # Lista mostrando apenas o nome
    search_fields = ('nome',)  # Campo de busca