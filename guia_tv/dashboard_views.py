from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from guia_tv.services.sync_service import SyncService

from .models import (
    Category,
    Channel,
    Country,
    IPTVSource,
    Language,
)


# Antes: dashboard y sync_channels eran públicos, sin ningún control
# de acceso -> cualquier visitante podía ver estadísticas internas y
# disparar una sincronización IPTV completa.

@login_required
@user_passes_test(lambda u: u.is_staff)
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


@login_required
@user_passes_test(lambda u: u.is_staff)
@require_POST
def sync_channels(request):

    total = SyncService.sync()

    messages.success(
        request,
        f"{total} canales sincronizados correctamente."
    )

    return redirect("dashboard")
