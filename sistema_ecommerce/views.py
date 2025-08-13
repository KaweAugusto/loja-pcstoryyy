# sistema_ecommerce/views.py
from django.views.generic import ListView
from produto.models import Produto

class HomeView(ListView):
    """
    Esta é a view da sua página inicial.
    Ela busca os 4 produtos mais recentes para exibir na seção "Produtos em Destaque".
    """
    model = Produto
    template_name = 'home.html'
    context_object_name = 'produtos'

    def get_queryset(self):
        """ Retorna os 4 produtos mais recentes que estão disponíveis. """
        return Produto.objects.filter(disponivel=True).order_by('-criado_em')[:4]