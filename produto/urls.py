# produto/urls.py
from django.urls import path
from .views import ProdutoListView, ProdutoDetailView

# Define um 'namespace' para as URLs deste app.
app_name = 'produto'

urlpatterns = [
    # URL para a lista de todos os produtos
    # Ex: /produto/
    path('', ProdutoListView.as_view(), name='lista'),

    # URL para a página de detalhes de um produto específico
    # Ex: /produto/1/
    path('<int:pk>/', ProdutoDetailView.as_view(), name='detail'),
]