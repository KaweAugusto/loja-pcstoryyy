# pedidos/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Pedido
from .forms import PedidoForm, ItemPedidoFormSet


class PedidoListView(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = 'pedidos/order_list.html'
    context_object_name = 'pedidos'
    ordering = ['-criado_em']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(cliente__user=self.request.user)


class PedidoDetailView(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = 'pedidos/order_detail.html'
    context_object_name = 'pedido'


class PedidoCreateView(LoginRequiredMixin, CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'pedidos/order_form.html'
    success_url = reverse_lazy('pedidos:lista')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ItemPedidoFormSet(self.request.POST)
        else:
            data['formset'] = ItemPedidoFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            # Assumindo que a relação user -> cliente existe
            form.instance.cliente = self.request.user.cliente
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class PedidoUpdateView(LoginRequiredMixin, UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'pedidos/order_form.html'
    success_url = reverse_lazy('pedidos:lista')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ItemPedidoFormSet(self.request.POST, instance=self.object)
        else:
            data['formset'] = ItemPedidoFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

# -----------------------------------------------------------------------------
# VIEWS DE CANCELAMENTO DE PEDIDO (ADICIONADAS)
# -----------------------------------------------------------------------------

@login_required
def solicitar_cancelamento(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    # Garante que apenas o dono do pedido pode solicitar o cancelamento
    if pedido.cliente.user == request.user:
        pedido.status_cancelamento = 'solicitado'
        pedido.save()
        messages.success(request, 'Sua solicitação de cancelamento foi enviada e será analisada.')
    else:
        messages.error(request, 'Você não tem permissão para realizar esta ação.')
    return redirect('pedidos:detalhar', pk=pedido.id)


@login_required
def status_cancelamento(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    # Página para o admin ver e decidir sobre o cancelamento
    if not request.user.is_superuser:
        messages.error(request, 'Acesso negado.')
        return redirect('pedidos:lista')
    return render(request, 'pedidos/status_cancelamento.html', {'pedido': pedido})


@login_required
def confirmar_cancelamento(request, pedido_id):
    # Ação que o admin toma para confirmar
    if not request.user.is_superuser:
        messages.error(request, 'Acesso negado.')
        return redirect('pedidos:lista')
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.status_cancelamento = 'cancelado'
    pedido.status = 'CANCELADO' # Muda o status principal do pedido também
    pedido.save()
    messages.success(request, f'O pedido #{pedido.id} foi cancelado com sucesso.')
    return redirect('pedidos:lista')


@login_required
def negar_cancelamento(request, pedido_id):
    # Ação que o admin toma para negar
    if not request.user.is_superuser:
        messages.error(request, 'Acesso negado.')
        return redirect('pedidos:lista')
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.status_cancelamento = 'recusado'
    pedido.save()
    messages.warning(request, f'A solicitação de cancelamento para o pedido #{pedido.id} foi negada.')
    return redirect('pedidos:lista')