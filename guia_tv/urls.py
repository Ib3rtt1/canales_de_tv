from django.urls import path

from . import dashboard_views
from guia_tv.views import home, channel_detail


urlpatterns = [

    path(
        "",
        home,
        name="home",
    ),

    path(
        "dashboard/",
        dashboard_views.dashboard,
        name="dashboard",
    ),

    path(
        "canal/<slug:slug>/",
        channel_detail,
        name="player",
    ),

    path(
        "dashboard/sync/",
        dashboard_views.sync_channels,
        name="sync_channels",
    ),

]