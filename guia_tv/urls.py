# guia_tv/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Raíz de la aplicación
    path('contacto/', views.contacto, name='contacto'),
]
