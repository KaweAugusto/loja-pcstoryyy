from django.contrib import admin
from .models import Produto, Categoria
from django.utils.html import format_html

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco', 'estoque', 'disponivel', 'preview_imagem')
    search_fields = ('nome',)
    list_filter = ('categoria', 'disponivel')
    list_editable = ('preco', 'estoque', 'disponivel')
    ordering = ('nome',)

    def preview_imagem(self, obj):
        """Exibe uma miniatura da imagem no admin"""
        if obj.imagem and hasattr(obj.imagem, 'url'):
            return format_html('<img src="{}" width="50" style="border-radius: 5px;" />', obj.imagem.url)
        return "—"
    preview_imagem.short_description = "Imagem"


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)