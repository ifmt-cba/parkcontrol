from django.urls import path

from .views import views_cobrancaDiaria


app_name = 'pagamentos'

urlpatterns = [
    path('listar/', views_cobrancaDiaria.listar_cobrancas, name='listar_cobranca'),
    path('atualizar/<int:cobranca_id>/', views_cobrancaDiaria.atualizar_status_cobranca, name='atualizar_status'),
    path('recibo/<int:cobranca_id>/', views_cobrancaDiaria.emitir_recibo, name='emitir_recibo'),
    ]