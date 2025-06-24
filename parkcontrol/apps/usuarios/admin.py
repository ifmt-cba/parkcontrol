from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from simple_history.admin import SimpleHistoryAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin, SimpleHistoryAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'perfil_acesso', 'is_active', 'is_staff')
    list_filter = ('perfil_acesso', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissões', {
            'fields': (
                'perfil_acesso',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        }),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'perfil_acesso', 'is_staff', 'is_active'),
        }),
    )
