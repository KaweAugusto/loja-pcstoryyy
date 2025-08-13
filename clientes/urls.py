# clientes/urls.py

from django.urls import path
from .views import (
    # Views de Autenticação
    login_registro_view,
    logout_view,
    minha_conta_view,

    # Views de Gerenciamento de Clientes (CRUD)
    ClienteListView,
    ClienteDetailView,
    ClienteCreateView,
    ClienteUpdateView,
    ClienteDeleteView,
)

app_name = 'clientes'

urlpatterns = [
    # URLs de Autenticação
    path('login-registro/', login_registro_view, name='login_registro'),
    path('sair/', logout_view, name='logout'),
    path('minha-conta/', minha_conta_view, name='minha_conta'),

    # URLs de Gerenciamento de Clientes (CRUD)
    path('', ClienteListView.as_view(), name='lista'),
    path('novo/', ClienteCreateView.as_view(), name='criar'),
    path('<int:pk>/', ClienteDetailView.as_view(), name='detalhar'),
    path('<int:pk>/editar/', ClienteUpdateView.as_view(), name='editar'),
    path('<int:pk>/apagar/', ClienteDeleteView.as_view(), name='apagar'),
]