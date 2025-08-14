from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from produto.models import Produto
from .models import Carrinho, ItemCarrinho
from django.contrib import messages


def _get_carrinho(request):
    """Função auxiliar para obter ou criar o carrinho."""
    if request.user.is_authenticated:
        carrinho, created = Carrinho.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        carrinho, created = Carrinho.objects.get_or_create(session_key=session_key)
    return carrinho


@require_POST
def adicionar_ao_carrinho(request, produto_id):
    carrinho = _get_carrinho(request)
    produto = get_object_or_404(Produto, id=produto_id)

    # Verifica se o item já está no carrinho
    item, created = ItemCarrinho.objects.get_or_create(
        carrinho=carrinho,
        produto=produto
    )

    if not created:
        item.quantidade += 1
        item.save()
        messages.success(request, f'Mais uma unidade de "{produto.nome}" foi adicionada ao seu carrinho.')
    else:
        messages.success(request, f'"{produto.nome}" foi adicionado ao seu carrinho.')

    return redirect('carrinho:detalhe')


def detalhe_carrinho(request):
    carrinho = _get_carrinho(request)
    return render(request, 'carrinho/detalhe.html', {'carrinho': carrinho})


def remover_do_carrinho(request, item_id):
    item = get_object_or_404(ItemCarrinho, id=item_id)
    # Garante que o usuário só pode remover itens do seu próprio carrinho
    carrinho = _get_carrinho(request)
    if item.carrinho == carrinho:
        produto_nome = item.produto.nome
        item.delete()
        messages.info(request, f'"{produto_nome}" foi removido do seu carrinho.')
    return redirect('carrinho:detalhe')