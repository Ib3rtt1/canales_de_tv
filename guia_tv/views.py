from django.shortcuts import render

# Create your views here.
# guia_tv/views.py
from django.http import HttpResponse


def index(request):
    return HttpResponse("Bienvenido a la guía de TV")


def index(request):
    return render(request, 'guia_tv/index.html')


def contacto(request):
    return render(request, 'guia_tv/contacto.html')
