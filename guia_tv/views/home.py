from django.db.models import Count, Prefetch
from django.shortcuts import render

from guia_tv.models import (
    Category,
    Channel,
    Country,
)


def home(request):
    """
    Página principal de TV Online
    """

    featured_channels = (
        Channel.objects
        .filter(
            is_active=True,
            is_featured=True,
        )
        .select_related(
            "country",
            "category",
            "language",
        )
        .order_by("-views")[:8]
    )

    latest_channels = (
        Channel.objects
        .filter(is_active=True)
        .select_related(
            "country",
            "category",
            "language",
        )
        .order_by("-created_at")[:12]
    )

    popular_channels = (
        Channel.objects
        .filter(is_active=True)
        .select_related(
            "country",
            "category",
            "language",
        )
        .order_by("-views")[:12]
    )

    countries = (
        Country.objects
        .annotate(
            total=Count("channels")
        )
        .order_by("name")
    )

    categories = (
        Category.objects
        .prefetch_related(
            Prefetch(
                "channels",
                queryset=Channel.objects.filter(
                    is_active=True
                )
                .select_related(
                    "country",
                    "category",
                    "language",
                )
                .order_by("name")
            )
        )
        .order_by("name")
    )

    total_channels = (
        Channel.objects
        .filter(is_active=True)
        .count()
    )

    total_categories = (
        Category.objects
        .count()
    )

    total_countries = (
        Country.objects
        .count()
    )

    context = {

        "featured_channels": featured_channels,

        "latest_channels": latest_channels,

        "popular_channels": popular_channels,

        "countries": countries,

        "categories": categories,

        "total_channels": total_channels,

        "total_categories": total_categories,

        "total_countries": total_countries,

    }

    return render(
        request,
        "guia_tv/index.html",
        context,
    )