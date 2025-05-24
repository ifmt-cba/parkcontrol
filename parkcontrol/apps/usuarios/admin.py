# apps/usuarios/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('username', 'email', 'first_name', 'last_name', 'perfil_acesso', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Informações de Perfil', {'fields': ('perfil_acesso',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações de Perfil', {'fields': ('perfil_acesso',)}),
    )

admin.site.register(Usuario, UsuarioAdmin)
