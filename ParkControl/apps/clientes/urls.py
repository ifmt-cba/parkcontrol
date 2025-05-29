from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_clientes_view, name='cadastrar_cliente'),
    path('mensalista/', views.cadastro_mensalistas_view, name='cadastro_mensalista'),
    path('diarista/', views.cadastro_diaristas_view, name='cadastro_diarista'),
    path('mensalistas/', views.cliente_mensalista_view, name='cliente_mensalista'),
    path('diaristas/', views.cliente_diarista_view, name='cliente_diarista'),
    path('mensalista/editar/<int:pk>/', views.editar_mensalista_view, name='editar_mensalista'),
    path('diarista/editar/<int:pk>/', views.editar_diarista_view, name='editar_diarista'),
]
