from django.db.models import Count, Prefetch

from guia_tv.models import (
    Category,
    Channel,
    Country,
)

from guia_tv.services.channel_service import ChannelService


class HomeService:

    @staticmethod
    def get_home_context(country=None, category=None):

        channels = ChannelService.filtered_channels(
            country=country,
            category=category,
        )

        featured_channels = (
            channels
            .filter(is_featured=True)
            .order_by("-views")
        )

        latest_channels = (
            channels
            .order_by("-created_at")[:12]
        )

        popular_channels = (
            channels
            .order_by("-views")[:12]
        )

        countries = (
            Country.objects
            .annotate(total=Count("channels"))
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

        return {

            "hero_channel": featured_channels.first(),

            "featured_channels": featured_channels,

            "latest_channels": latest_channels,

            "popular_channels": popular_channels,

            "countries": countries,

            "categories": categories,

            "total_channels": channels.count(),

            "total_categories": Category.objects.count(),

            "total_countries": Country.objects.count(),

            "selected_country": country,

            "selected_category": category,

        }