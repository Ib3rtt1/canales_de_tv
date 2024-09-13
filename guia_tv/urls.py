# guia_tv/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Raíz de la aplicación
    path('contacto/', views.contacto, name='contacto'),
    # Nueva ruta para el carrusel
    path('carrusel_canales/', views.carrusel_canales, name='carrusel_canales'),
]
