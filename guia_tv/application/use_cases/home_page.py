from django.db.models import Count, Prefetch

from guia_tv.models import (
    Category,
    Country,
    Channel,
)

from guia_tv.repositories.channel_repository import (
    ChannelRepository,
)


class HomePageUseCase:

    def execute(self, filters=None):

        filters = filters or {}

        country_id = filters.get("country")
        category_id = filters.get("category")

        channels = ChannelRepository.active()

        if country_id:
            channels = channels.filter(
                country_id=country_id
            )

        if category_id:
            channels = channels.filter(
                category_id=category_id
            )

        featured_channels = (
            channels
            .filter(is_featured=True)
            .order_by("-views")
        )

        hero_channel = featured_channels.first()

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
                    queryset=ChannelRepository.active()
                )
            )
            .order_by("name")
        )

        return {

            "hero_channel": hero_channel,

            "featured_channels": featured_channels,

            "latest_channels": latest_channels,

            "popular_channels": popular_channels,

            "countries": countries,

            "categories": categories,

            "total_channels": channels.count(),

            "total_categories": Category.objects.count(),

            "total_countries": Country.objects.count(),

            "selected_country": country_id,

            "selected_category": category_id,

        }