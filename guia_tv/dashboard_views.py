from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from guia_tv.application.use_cases.add_channel import (
    AddChannelError,
    AddChannelInput,
    AddChannelUseCase,
)
from guia_tv.application.use_cases.import_playlist import SyncAllSourcesUseCase
from guia_tv.forms import AddChannelForm
from guia_tv.repositories.iptv_source_repository import IPTVSourceRepository

from .models import Category, Channel, Country, IPTVSource, Language

is_staff = user_passes_test(lambda u: u.is_staff)


# Antes: dashboard y sync_channels eran públicos, sin ningún control de
# acceso -> cualquier visitante podía ver estadísticas internas y
# disparar una sincronización IPTV completa. Se mantiene el mismo
# criterio de acceso (login + staff) para las vistas nuevas.

@login_required
@is_staff
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

        "pending_channels": Channel.objects.filter(
            license_status="pending"
        ).count(),

        "pending_sources": IPTVSourceRepository.pending_review().count(),

    }

    return render(
        request,
        "dashboard/index.html",
        context,
    )


@login_required
@is_staff
@require_POST
def sync_channels(request):

    # Antes: SyncService.sync() recorría IPTVSource.objects.filter(enabled=True)
    # sin mirar licencia -> cualquier fuente habilitada se sincronizaba,
    # aunque nadie hubiera confirmado que sus canales están autorizados.
    results = SyncAllSourcesUseCase().execute()

    total = SyncAllSourcesUseCase.total_imported(results)
    omitted = [r for r in results if not r.ok]

    messages.success(
        request,
        f"{total} canales sincronizados correctamente.",
    )

    if omitted:
        nombres = ", ".join(r.source_name for r in omitted)
        messages.warning(
            request,
            f"{len(omitted)} fuente(s) omitida(s) por licencia/errores: {nombres}.",
        )

    return redirect("dashboard")


@login_required
@is_staff
def add_channel(request):

    if request.method == "POST":
        form = AddChannelForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            try:
                channel = AddChannelUseCase().execute(
                    AddChannelInput(
                        name=data["name"],
                        stream_url=data["stream_url"],
                        license_status=data["license_status"],
                        license_note=data["license_note"],
                        website=data.get("website", ""),
                        logo_url=data.get("logo_url", ""),
                        country_id=data["country"].id if data.get("country") else None,
                        language_id=data["language"].id if data.get("language") else None,
                        category_id=data["category"].id if data.get("category") else None,
                        quality=data["quality"],
                        skip_url_check=data.get("skip_url_check", False),
                    )
                )
            except AddChannelError as exc:
                form.add_error(None, str(exc))
            else:
                messages.success(
                    request,
                    f"Canal '{channel.name}' agregado correctamente.",
                )
                return redirect("dashboard")
    else:
        form = AddChannelForm()

    return render(
        request,
        "dashboard/add_channel.html",
        {"form": form},
    )
