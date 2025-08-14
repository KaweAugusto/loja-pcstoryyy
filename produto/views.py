from django.db.models import Q
from django.views.generic import ListView, DetailView
from .models import Produto, Categoria


class ProdutoListView(ListView):
    model = Produto
    template_name = 'produto/produtos_list.html'
    context_object_name = 'produtos'
    paginate_by = 9

    def get_queryset(self):
        """
        Este método filtra os produtos.
        Ele mostra apenas os produtos disponíveis e aplica os filtros de busca e categoria.
        """
        # Começa com todos os produtos que estão marcados como disponíveis
        queryset = Produto.objects.filter(disponivel=True)

        # Pega o ID da categoria da URL
        categoria_id = self.request.GET.get('categoria')
        if categoria_id:
            queryset = queryset.filter(categoria__id=categoria_id)

        # Pega o termo de busca da URL
        query = self.request.GET.get('q')
        if query:
            # Filtra por nome OU descrição
            queryset = queryset.filter(
                Q(nome__icontains=query) | Q(descricao__icontains=query)
            )

        return queryset.order_by('nome')

    def get_context_data(self, **kwargs):
        """
        Adiciona a lista de todas as categorias ao contexto para que
        possamos exibi-las no filtro da página.
        """
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context


class ProdutoDetailView(DetailView):
    model = Produto
    template_name = 'produto/produtos_detail.html'
    context_object_name = 'produto'