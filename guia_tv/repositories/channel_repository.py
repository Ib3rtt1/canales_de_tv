from django.db.models import QuerySet

from guia_tv.models import Channel


class ChannelRepository:

    @staticmethod
    def all() -> QuerySet:
        return (
            Channel.objects
            .select_related(
                "country",
                "category",
                "language",
            )
        )

    @staticmethod
    def active() -> QuerySet:
        return (
            ChannelRepository
            .all()
            .filter(is_active=True)
        )

    @staticmethod
    def featured() -> QuerySet:
        return (
            ChannelRepository
            .active()
            .filter(is_featured=True)
        )

    @staticmethod
    def latest(limit=12) -> QuerySet:
        return (
            ChannelRepository
            .active()
            .order_by("-created_at")[:limit]
        )

    @staticmethod
    def popular(limit=12) -> QuerySet:
        return (
            ChannelRepository
            .active()
            .order_by("-views")[:limit]
        )

    @staticmethod
    def by_slug(slug):
        return (
            ChannelRepository
            .active()
            .filter(slug=slug)
            .first()
        )

    @staticmethod
    def by_country(country_id):
        return (
            ChannelRepository
            .active()
            .filter(country_id=country_id)
        )

    @staticmethod
    def by_category(category_id):
        return (
            ChannelRepository
            .active()
            .filter(category_id=category_id)
        )

    @staticmethod
    def search(text):
        return (
            ChannelRepository
            .active()
            .filter(name__icontains=text)
        )