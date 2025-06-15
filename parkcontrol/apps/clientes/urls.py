from django.urls import path
from . import views

app_name = 'clientes'  # Define o namespace para o app clientes

urlpatterns = [
    path('cadastrar/', views.cadastrar_clientes_view, name='cadastrar_cliente'),
    path('mensalista/', views.cadastro_mensalistas_view, name='cadastro_mensalista'),
    path('diarista/', views.cadastro_diaristas_view, name='cadastro_diarista'),
    path('mensalistas/', views.cliente_mensalista_view, name='cliente_mensalista'),
    path('diaristas/', views.cliente_diarista_view, name='cliente_diarista'),
    path('mensalista/editar/<int:pk>/', views.editar_mensalista_view, name='editar_mensalista'),
    path('diarista/editar/<int:pk>/', views.editar_diarista_view, name='editar_diarista'),
    path('mensalista/excluir/<int:pk>/', views.excluir_mensalista_view, name='excluir_mensalista'),
    path('diarista/excluir/<int:pk>/', views.excluir_diarista_view, name='excluir_diarista'),
    path('diarista/inativar/<int:pk>/', views.inativar_diarista_view, name='inativar_diarista'),
    path('diarista/ativar/<int:pk>/', views.ativar_diarista_view, name='ativar_diarista'),
    path('mensalistas/excluir/<int:pk>/', views.excluir_mensalista_view, name='excluir_mensalista'),
    path('mensalistas/ativar/<int:pk>/', views.ativar_mensalista_view, name='ativar_mensalista'),
    path('mensalistas/inativar/<int:pk>/', views.inativar_mensalista_view, name='inativar_mensalista'),
]
