from guia_tv.models import Channel


class ChannelService:

    @staticmethod
    def filtered_channels(country=None,
        category=None,
        language=None,
        quality=None,
        status=None,
        search=None,
        featured=None,):

        queryset = (
            Channel.objects
            .filter(is_active=True)
            .select_related(
                "country",
                "category",
                "language",
            )
        )

        if country:
            queryset = queryset.filter(country_id=country)

        if category:
            queryset = queryset.filter(category_id=category)

        return queryset