from django.urls import path
from . import views

app_name = 'carrinho'

urlpatterns = [
    path('', views.detalhe_carrinho, name='detalhe'),
    path('adicionar/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar'),
    path('remover/<int:item_id>/', views.remover_do_carrinho, name='remover'),
]