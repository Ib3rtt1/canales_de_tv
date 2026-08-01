from django.db.models import F
from django.shortcuts import get_object_or_404, render

from ..models import Channel
from ..repositories.channel_repository import ChannelRepository


def channel_detail(request, slug):
    """
    Reproductor de un canal IPTV.
    """

    # Antes: is_active=True, sin mirar la licencia -> se podía reproducir
    # (y contar vistas de) un canal "pending"/"rejected" con solo
    # conocer su slug.
    channel = get_object_or_404(
        ChannelRepository.publishable(),
        slug=slug,
    )

    # Incrementar contador de vistas
    Channel.objects.filter(pk=channel.pk).update(
        views=F("views") + 1
    )

    channel.refresh_from_db()

    # Canales relacionados
    related_channels = (
        ChannelRepository.publishable()
        .filter(category=channel.category)
        .exclude(pk=channel.pk)
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