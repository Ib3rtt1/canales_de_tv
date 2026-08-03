from django.db.models import F
from django.shortcuts import get_object_or_404, render

from ..models import Channel
from ..repositories.channel_repository import ChannelRepository


def channel_detail(request, slug):
    """
    Reproductor de un canal IPTV.
    """

    # Obtener el canal
    channel = get_object_or_404(
        ChannelRepository.publishable(),
        slug=slug,
    )

    # Incrementar vistas
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

    # Todos los canales (para la barra lateral)
    all_channels = (
        Channel.objects
        .filter(is_active=True)
        .select_related(
            "country",
            "category",
            "language",
        )
        .order_by("pk")
    )
    channel_list = list(all_channels)

    current_index = next(
        (
            index
            for index, item in enumerate(channel_list)
            if item.id == channel.id
        ),
        0,
    )

    total = len(channel_list)

    previous_channel = channel_list[(current_index - 1) % total]

    next_channel = channel_list[(current_index + 1) % total]
    
    context = {
        "channel": channel,
        "related_channels": related_channels,
        "all_channels": all_channels,
        "previous_channel": previous_channel,
        "next_channel": next_channel,
    }

    return render(
        request,
        "guia_tv/player.html",
        context,
    )