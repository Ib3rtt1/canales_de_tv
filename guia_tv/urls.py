from django.urls import path

from . import dashboard_views
# Se agrega stream_proxy a las vistas importadas de guia_tv.views:
from guia_tv.views import (
    home,
    channel_detail,
    search_channels,
    stream_proxy,  # <--- Agregado aquí
)

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
        "buscar/",
        search_channels,
        name="search",
    ),
    path(
        "dashboard/sync/",
        dashboard_views.sync_channels,
        name="sync_channels",
    ),
    path(
        "dashboard/canales/nuevo/",
        dashboard_views.add_channel,
        name="add_channel",
    ),
    path(
        "channel/<int:channel_id>/stream/",
        stream_proxy,
        name="stream_proxy",
    ),
]