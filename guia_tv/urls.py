from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("canal/<slug:slug>/", views.channel_detail, name="player"),
]