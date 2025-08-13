# clientes/views.py

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import ProtectedError

from .models import Cliente
from .forms import ClienteCreationForm, LoginForm, ClienteForm


def login_registro_view(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    login_form = LoginForm(request.POST or None)
    register_form = ClienteCreationForm(request.POST or None)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'register':
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                messages.success(request, 'Cadastro realizado com sucesso!')
                return redirect(settings.LOGIN_REDIRECT_URL)

        elif action == 'login':
            if login_form.is_valid():
                username_or_email = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(request, username=username_or_email, password=password)

                if user is None and '@' in username_or_email:
                    try:
                        user_obj = User.objects.get(email=username_or_email)
                        user = authenticate(request, username=user_obj.username, password=password)
                    except User.DoesNotExist:
                        user = None

                if user is not None:
                    login(request, user)
                    return redirect(settings.LOGIN_REDIRECT_URL)
                else:
                    messages.error(request, 'Usuário ou senha inválidos.')

    context = {
        'login_form': login_form,
        'register_form': register_form
    }
    return render(request, 'login_registro.html', context)


def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu da sua conta.')
    return redirect('home')


@login_required
def minha_conta_view(request):
    return render(request, 'clientes/minha_conta.html')


class ClienteListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Cliente
    template_name = 'clientes/client_list.html'
    context_object_name = 'clientes'

    def test_func(self):
        return self.request.user.is_superuser


class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = 'clientes/client_detail.html'
    context_object_name = 'cliente'


class ClienteCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/client_form.html'
    success_url = reverse_lazy('clientes:lista')

    def test_func(self):
        return self.request.user.is_superuser


class ClienteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/client_form.html'
    success_url = reverse_lazy('clientes:lista')

    def test_func(self):
        return self.request.user.is_superuser


class ClienteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Cliente
    template_name = 'clientes/client_confirm_delete.html'
    success_url = reverse_lazy('clientes:lista')

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            cliente = self.get_object()
            messages.error(request,
                           f'Não é possível excluir o cliente {cliente.nome}, pois ele possui pedidos vinculados.')
            return redirect('clientes:lista')

    def test_func(self):
        return self.request.user.is_superuser