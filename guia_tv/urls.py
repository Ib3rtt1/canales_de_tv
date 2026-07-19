from django.urls import path

from . import views
from . import dashboard_views

urlpatterns = [

    path("", views.home, name="home"),

    path(
        "dashboard/",
        dashboard_views.dashboard,
        name="dashboard",
    ),

    path(
        "canal/<slug:slug>/",
        views.channel_detail,
        name="player",
    ),
    path(
    "dashboard/sync/",
    dashboard_views.sync_channels,
    name="sync_channels", 
    ),

]

