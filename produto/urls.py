# produto/urls.py
from django.urls import path
from .views import (
    ProdutoListView,
    ProdutoDetailView,
    ProdutoCreateView,
    ProdutoUpdateView,
    ProdutoDeleteView
)

app_name = 'produto'

urlpatterns = [
    # Lista todos os produtos
    path('', ProdutoListView.as_view(), name='lista'),

    # Cria um novo produto
    path('novo/', ProdutoCreateView.as_view(), name='create'),

    # Detalhes de um produto específico
    path('<int:pk>/', ProdutoDetailView.as_view(), name='detail'),

    # Edita um produto existente
    path('<int:pk>/editar/', ProdutoUpdateView.as_view(), name='update'),

    # Deleta um produto
    path('<int:pk>/deletar/', ProdutoDeleteView.as_view(), name='delete'),
]