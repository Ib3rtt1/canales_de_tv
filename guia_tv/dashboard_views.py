from django.shortcuts import render

from django.contrib import messages
from django.shortcuts import redirect

from guia_tv.services.sync_service import SyncService

from .models import (
    Category,
    Channel,
    Country,
    IPTVSource,
    Language,
)


def dashboard(request):

    context = {

        "channels": Channel.objects.count(),

        "countries": Country.objects.count(),

        "categories": Category.objects.count(),

        "languages": Language.objects.count(),

        "sources": IPTVSource.objects.count(),

        "active_channels": Channel.objects.filter(
            is_active=True
        ).count(),

    }

    return render(
        request,
        "dashboard/index.html",
        context,
    )




def sync_channels(request):

    total = SyncService.sync()

    messages.success(
        request,
        f"{total} canales sincronizados correctamente."
    )

    return redirect("dashboard")