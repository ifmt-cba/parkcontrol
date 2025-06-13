from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('recuperar-senha/', views.recuperar_senha, name='recuperar_senha'),
]
