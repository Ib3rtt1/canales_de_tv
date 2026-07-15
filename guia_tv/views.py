from django.shortcuts import get_object_or_404, render

from .models import Category, Channel


def home(request):
    categories = (
        Category.objects.prefetch_related("channels")
        .order_by("name")
    )

    context = {
        "categories": categories
    }

    return render(request, "guia_tv/index.html", context)


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