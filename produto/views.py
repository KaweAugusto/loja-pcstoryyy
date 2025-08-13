# produto/views.py
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Produto, Categoria
from .forms import ProdutoForm

# A HomeView foi removida daqui para evitar conflitos.

class ProdutoListView(ListView):
    model = Produto
    template_name = 'produto/produtos_list.html'
    context_object_name = 'produtos'
    paginate_by = 9

    def get_queryset(self):
        queryset = Produto.objects.filter(disponivel=True)
        categoria_id = self.request.GET.get('categoria')
        if categoria_id:
            queryset = queryset.filter(categoria__id=categoria_id)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(nome__icontains=query) | Q(descricao__icontains=query))
        return queryset.order_by('nome')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context

class ProdutoDetailView(DetailView):
    model = Produto
    template_name = 'produto/produtos_detail.html'
    context_object_name = 'produto'

class ProdutoCreateView(LoginRequiredMixin, CreateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'produto/produtos_form.html'
    success_url = reverse_lazy('produto:lista')

class ProdutoUpdateView(LoginRequiredMixin, UpdateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'produto/produtos_form.html'
    success_url = reverse_lazy('produto:lista')

class ProdutoDeleteView(LoginRequiredMixin, DeleteView):
    model = Produto
    template_name = 'produto/produtos_confirm_delete.html'
    success_url = reverse_lazy('produto:lista')