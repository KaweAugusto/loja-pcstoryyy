from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.db import transaction
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from datetime import date, timedelta

from .models import Pedido, ItemPedido
from carrinho.models import Carrinho
from clientes.models import Cliente


class PedidoListView(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = 'pedidos/order_list.html'
    context_object_name = 'pedidos'
    ordering = ['-criado_em']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Pedido.objects.all()
        return Pedido.objects.filter(cliente__user=user)


class PedidoDetailView(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = 'pedidos/order_detail.html'
    context_object_name = 'pedido'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Pedido.objects.all()
        return Pedido.objects.filter(cliente__user=user)


@login_required
def finalizar_pedido(request):
    try:
        carrinho = request.user.carrinho
        if not carrinho.itens.all().exists():
            messages.warning(request, "Seu carrinho está vazio.")
            return redirect('carrinho:detalhe')
    except Carrinho.DoesNotExist:
        messages.error(request, "Ocorreu um erro ao encontrar seu carrinho.")
        return redirect('home')

    if request.method == 'POST':
        cliente, created = Cliente.objects.get_or_create(
            user=request.user,
            defaults={'nome': request.user.get_full_name() or request.user.username}
        )

        with transaction.atomic():
            novo_pedido = Pedido.objects.create(
                cliente=cliente,
                total=carrinho.total,
                status='AGUARDANDO_PAGAMENTO'
            )

            for item_carrinho in carrinho.itens.all():
                ItemPedido.objects.create(
                    pedido=novo_pedido,
                    produto=item_carrinho.produto,
                    quantidade=item_carrinho.quantidade,
                    preco=item_carrinho.produto.preco
                )

            carrinho.itens.all().delete()

            assunto = f"Confirmação do seu Pedido #{novo_pedido.id} na PC-Store"
            corpo_html = render_to_string('pedidos/email_confirmacao_pedido.html',
                                          {'pedido': novo_pedido, 'user': request.user, 'request': request})
            send_mail(
                assunto, '',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                html_message=corpo_html
            )

            return redirect('pedidos:sucesso', pedido_id=novo_pedido.id)

    return render(request, 'pedidos/finalizar_pedido.html', {'carrinho': carrinho})


@login_required
def pedido_sucesso(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente__user=request.user)
    return render(request, 'pedidos/pedido_sucesso.html', {'pedido': pedido})


@login_required
def ver_boleto(request, pedido_id):
    user = request.user
    if user.is_staff:
        pedido = get_object_or_404(Pedido, id=pedido_id)
    else:
        pedido = get_object_or_404(Pedido, id=pedido_id, cliente__user=user)

    data_vencimento = pedido.criado_em.date() + timedelta(days=5)

    context = {
        'pedido': pedido,
        'data_vencimento': data_vencimento
    }
    return render(request, 'pedidos/boleto.html', context)


# --- AQUI ESTÁ A CORREÇÃO ---
@login_required
def solicitar_cancelamento(request, pedido_id):
    user = request.user

    # Se o usuário for admin, busca o pedido apenas pelo ID
    if user.is_staff:
        pedido = get_object_or_404(Pedido, id=pedido_id)
        # Admin pode cancelar diretamente
        if request.method == 'POST':
            pedido.status = 'CANCELADO'
            pedido.save()
            messages.success(request, f"O Pedido #{pedido.id} foi cancelado pelo administrador.")
        else:
            messages.error(request, "Método inválido.")

    # Se for um cliente normal, busca pelo ID E garante que o pedido é dele
    else:
        pedido = get_object_or_404(Pedido, id=pedido_id, cliente__user=user)
        if pedido.status == 'AGUARDANDO_PAGAMENTO':
            if request.method == 'POST':
                pedido.status = 'CANCELAMENTO_SOLICITADO'
                pedido.save()
                messages.success(request, f"Sua solicitação para cancelar o Pedido #{pedido.id} foi enviada.")
            else:
                messages.error(request, "Método inválido.")
        else:
            messages.error(request, f"Não é mais possível solicitar o cancelamento para o Pedido #{pedido.id}.")

    return redirect('pedidos:lista')