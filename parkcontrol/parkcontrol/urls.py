from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.usuarios.urls', namespace='usuarios')),
    path('planos/', include('apps.planos.urls', namespace='planos')),
    path('frentistas/', include('apps.frentistas.urls', namespace='frentistas')),
    path('clientes/', include('apps.clientes.urls', namespace='clientes')),
    path('gestao-pagamentos/', include('apps.pagamentos.urls', namespace='pagamentos')),
]
