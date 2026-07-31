from django.db.models import F
from django.shortcuts import get_object_or_404, render

from ..models import Channel


def channel_detail(request, slug):
    """
    Reproductor de un canal IPTV.
    """

    channel = get_object_or_404(
        Channel.objects.select_related(
            "country",
            "category",
            "language",
        ),
        slug=slug,
        is_active=True,
    )

    # Incrementar contador de vistas
    Channel.objects.filter(pk=channel.pk).update(
        views=F("views") + 1
    )

    channel.refresh_from_db()

    # Canales relacionados
    related_channels = (
        Channel.objects.filter(
            category=channel.category,
            is_active=True,
        )
        .exclude(pk=channel.pk)
        .select_related(
            "country",
            "category",
            "language",
        )
        .order_by("-views")[:10]
    )

    context = {
        "channel": channel,
        "related_channels": related_channels,
    }

    return render(
        request,
        "guia_tv/player.html",
        context,
    )