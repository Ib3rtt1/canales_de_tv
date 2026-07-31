from django.utils import timezone

from guia_tv.models import Program


class ProgramRepository:

    @staticmethod
    def current(channel):

        now = timezone.now()

        return (
            Program.objects
            .filter(
                channel=channel,
                start__lte=now,
                end__gte=now,
            )
            .first()
        )

    @staticmethod
    def next(channel):

        now = timezone.now()

        return (
            Program.objects
            .filter(
                channel=channel,
                start__gt=now,
            )
            .order_by("start")
            .first()
        )

    @staticmethod
    def today(channel):

        return (
            Program.objects
            .filter(channel=channel)
            .order_by("start")
        )