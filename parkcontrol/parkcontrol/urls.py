from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.usuarios.urls', namespace='usuarios')),
    path('planos/', include('apps.planos.urls', namespace='planos')),
    path('frentistas/', include('apps.frentistas.urls', namespace='frentistas')),
    path('clientes/', include('apps.clientes.urls', namespace='clientes')),
    path('vagas/', include('apps.vagas.urls', namespace='vagas')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('manutencao/', include('apps.manutencao.urls', namespace='manutencao')),
]
