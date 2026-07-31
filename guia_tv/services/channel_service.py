from guia_tv.models import Channel


class ChannelService:

    @staticmethod
    def filtered_channels(
        country=None,
        category=None,
        language=None,
        quality=None,
        status=None,
        search=None,
        featured=None,
    ):

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

        # Antes: estos filtros se recibían pero nunca se aplicaban.
        if language:
            queryset = queryset.filter(language_id=language)

        if quality:
            queryset = queryset.filter(quality=quality)

        if status:
            queryset = queryset.filter(status=status)

        if search:
            queryset = queryset.filter(name__icontains=search)

        if featured is not None:
            queryset = queryset.filter(is_featured=featured)

        return queryset
