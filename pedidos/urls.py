# pedidos/urls.py
from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    # URL para a lista de pedidos do cliente
    # Ex: /pedidos/
    path('', views.PedidoListView.as_view(), name='lista'),

    # URL para ver os detalhes de um pedido específico
    # Ex: /pedidos/1/
    path('<int:pk>/', views.PedidoDetailView.as_view(), name='detalhe'),

    # URL para a página de finalização de compra
    # Ex: /pedidos/finalizar/
    path('finalizar/', views.finalizar_pedido, name='finalizar'),

    # URL para a página de sucesso após o pedido ser concluído
    # Ex: /pedidos/sucesso/1/
    path('sucesso/<int:pedido_id>/', views.pedido_sucesso, name='sucesso'),

    # Boleto
    path('boleto/<int:pedido_id>/', views.ver_boleto, name='ver_boleto'),

    # Solicitação de Cancelamento
    path('<int:pedido_id>/solicitar-cancelamento/', views.solicitar_cancelamento, name='solicitar_cancelamento'),
]