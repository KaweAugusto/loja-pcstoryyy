from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'endereco', 'user')

    def has_module_permission(self, request):
        return request.user.is_superuser  # só superuser vê no admin

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser
