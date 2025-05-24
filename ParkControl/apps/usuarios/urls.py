from django.urls import path
from . import views

urlpatterns = [
    path('recuperar-senha/', views.recuperar_senha, name='recuperar_senha'),
]
