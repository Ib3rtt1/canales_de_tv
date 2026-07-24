from django.shortcuts import get_object_or_404, render

from guia_tv.models import Channel


def channel_detail(request, slug):

    channel = get_object_or_404(
        Channel,
        slug=slug,
    )

    return render(
        request,
        "guia_tv/player.html",
        {
            "channel": channel,
        },
    )



def channel_detail(request, slug):

    channel = get_object_or_404(
        Channel,
        slug=slug,
        is_active=True
    )

    channel.views += 1
    channel.save(update_fields=["views"])

    context = {
        "channel": channel
    }

    return render(request, "guia_tv/player.html", context)