from django.urls import path
from .views import LoginRegistroView, logout_view, MinhaContaView

app_name = 'clientes'

urlpatterns = [
    # URL para a página que combina login e registro
    path('login-registro/', LoginRegistroView.as_view(), name='login_registro'),

    # URL para fazer o logout do usuário
    path('logout/', logout_view, name='logout'),

    # URL para a página de "Minha Conta", onde o usuário logado pode editar seus dados
    path('minha-conta/', MinhaContaView.as_view(), name='minha_conta'),
]