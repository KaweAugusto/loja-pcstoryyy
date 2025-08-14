from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cliente
from .forms import UserEditForm, ClienteForm


class LoginRegistroView(View):
    template_name = 'clientes/login_registro.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')

        if action == 'register':
            # --- Lógica de Registro ---
            nome_completo = request.POST.get('nome_completo')
            email = request.POST.get('email')
            senha = request.POST.get('senha')
            confirmar_senha = request.POST.get('confirmar_senha')
            endereco = request.POST.get('endereco')

            if not all([nome_completo, email, senha, confirmar_senha, endereco]):
                messages.error(request, 'Todos os campos são obrigatórios para o registro.')
                return render(request, self.template_name)

            if senha != confirmar_senha:
                messages.error(request, 'As senhas não coincidem.')
                return render(request, self.template_name)

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Este e-mail já está cadastrado.')
                return render(request, self.template_name)

            try:
                user = User.objects.create_user(username=email, email=email, password=senha)
                user.first_name = nome_completo.split(' ')[0]
                user.last_name = ' '.join(nome_completo.split(' ')[1:])
                user.save()

                Cliente.objects.create(user=user, nome=nome_completo, endereco=endereco)

                messages.success(request, 'Conta criada com sucesso! Faça o login para continuar.')
                return redirect('clientes:login_registro')

            except Exception as e:
                messages.error(request, f'Ocorreu um erro ao criar a conta: {e}')

        elif action == 'login':
            # --- Lógica de Login ---
            email = request.POST.get('email')
            password = request.POST.get('password')

            if not email or not password:
                messages.error(request, 'E-mail e senha são obrigatórios.')
                return render(request, self.template_name)

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'E-mail ou senha inválidos.')

        return render(request, self.template_name)


def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu da sua conta.')
    return redirect('home')


class MinhaContaView(LoginRequiredMixin, View):
    template_name = 'clientes/minha_conta.html'

    def get(self, request, *args, **kwargs):
        try:
            cliente = request.user.cliente
        except Cliente.DoesNotExist:
            cliente = Cliente.objects.create(user=request.user,
                                             nome=request.user.get_full_name() or request.user.username)

        user_form = UserEditForm(instance=request.user)
        cliente_form = ClienteForm(instance=cliente)

        context = {
            'user_form': user_form,
            'cliente_form': cliente_form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Garante que o cliente existe antes de tentar editar
        cliente, created = Cliente.objects.get_or_create(user=request.user, defaults={
            'nome': request.user.get_full_name() or request.user.username})

        user_form = UserEditForm(request.POST, instance=request.user)
        cliente_form = ClienteForm(request.POST, instance=cliente)

        if user_form.is_valid() and cliente_form.is_valid():
            user_form.save()
            cliente_form.save()
            messages.success(request, 'Sua conta foi atualizada com sucesso!')
            return redirect('clientes:minha_conta')

        context = {
            'user_form': user_form,
            'cliente_form': cliente_form
        }
        return render(request, self.template_name, context)