from django.db import models

from .channel import Channel


class Program(models.Model):

    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name="programs",
    )

    title = models.CharField(
        max_length=300,
    )

    subtitle = models.CharField(
        max_length=300,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    image = models.URLField(
        blank=True,
    )

    category = models.CharField(
        max_length=100,
        blank=True,
    )

    start = models.DateTimeField()

    end = models.DateTimeField()

    season = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    episode = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    rating = models.CharField(
        max_length=20,
        blank=True,
    )

    is_live = models.BooleanField(
        default=False,
    )

    class Meta:

        ordering = [
            "start",
        ]

        indexes = [
            models.Index(fields=["channel"]),
            models.Index(fields=["start"]),
            models.Index(fields=["end"]),
        ]

        verbose_name = "Programa"

        verbose_name_plural = "Programación"

    def __str__(self):
        return self.title