# pedidos/urls.py

from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    # URLs do CRUD de Pedidos
    path('', views.PedidoListView.as_view(), name='lista'),
    path('novo/', views.PedidoCreateView.as_view(), name='criar'),
    path('<int:pk>/', views.PedidoDetailView.as_view(), name='detalhar'),
    path('<int:pk>/editar/', views.PedidoUpdateView.as_view(), name='editar'),

    # URLs do Fluxo de Cancelamento
    path('<int:pedido_id>/solicitar-cancelamento/', views.solicitar_cancelamento, name='solicitar_cancelamento'),
    path('<int:pedido_id>/status-cancelamento/', views.status_cancelamento, name='status_cancelamento'),
    path('<int:pedido_id>/confirmar-cancelamento/', views.confirmar_cancelamento, name='confirmar_cancelamento'),
    path('<int:pedido_id>/negar-cancelamento/', views.negar_cancelamento, name='negar_cancelamento'),
]