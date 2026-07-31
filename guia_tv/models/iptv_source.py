from django.db import models
from django.utils import timezone



class IPTVSource(models.Model):

    name = models.CharField(
        max_length=150
    )

    url = models.URLField(
        unique=True
    )

    enabled = models.BooleanField(
        default=True
    )

    auto_update = models.BooleanField(
        default=True
    )

    priority = models.PositiveIntegerField(
        default=1
    )

    total_channels = models.PositiveIntegerField(
        default=0
    )

    last_update = models.DateTimeField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["priority", "name"]
        verbose_name = "Fuente IPTV"
        verbose_name_plural = "Fuentes IPTV"

    def mark_updated(self):

        self.last_update = timezone.now()

        self.save(update_fields=["last_update"])

    def __str__(self):
        return self.name