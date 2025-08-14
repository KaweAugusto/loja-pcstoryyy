from .models import Carrinho, ItemCarrinho

def carrinho(request):
    """
    Torna o objeto do carrinho e a contagem de itens disponíveis em todos os templates.
    """
    carrinho_obj = None
    count = 0
    if request.user.is_authenticated:
        carrinho_obj, created = Carrinho.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        carrinho_obj, created = Carrinho.objects.get_or_create(session_key=session_key)

    if carrinho_obj:
        count = carrinho_obj.itens.count()

    return {'carrinho': carrinho_obj, 'itens_carrinho_count': count}