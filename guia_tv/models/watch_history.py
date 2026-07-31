from django.contrib.auth.models import User
from django.db import models

from .channel import Channel


class WatchHistory(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE
    )

    watched_at = models.DateTimeField(
        auto_now=True
    )

    seconds = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ["-watched_at"]
        verbose_name = "Historial"
        verbose_name_plural = "Historial"

    def __str__(self):
        return f"{self.user.username} - {self.channel.name}"