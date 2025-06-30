from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.usuarios.urls', namespace='usuarios')),
    path('planos/', include('apps.planos.urls', namespace='planos')),
    path('frentistas/', include('apps.frentistas.urls', namespace='frentistas')),
    path('clientes/', include('apps.clientes.urls', namespace='clientes')),
    path('vagas/', include('apps.vagas.urls', namespace='vagas')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('manutencao/', include('apps.manutencao.urls', namespace='manutencao')),
    path('pagamentos/', include('apps.pagamentos.urls', namespace='pagamentos')),
    path('relatorios/', include('apps.relatorios.urls', namespace='relatorios')),

] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)