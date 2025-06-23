from django.urls import path
from . import views

app_name = 'relatorios'

urlpatterns = [
    path('', views.relatorios, name='dashboard_relatorios'),
]
