from django.urls import path
from . import views

app_name = 'manutencao'

urlpatterns = [
    path('', views.manutencao_dashboard, name='manutencao_dashboard'),
]