from django.db import models

from .channel import Channel


class ChannelStream(models.Model):

    STREAM_TYPES = [
        ("HLS", "HLS (.m3u8)"),
        ("MPD", "MPEG-DASH"),
        ("TS", "MPEG-TS"),
        ("RTMP", "RTMP"),
        ("OTHER", "Otro"),
    ]

    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name="streams",
    )

    name = models.CharField(
        max_length=200,
        default="Principal",
    )

    url = models.URLField(
        max_length=1000,
    )

    stream_type = models.CharField(
        max_length=20,
        choices=STREAM_TYPES,
        default="HLS",
    )

    priority = models.PositiveSmallIntegerField(
        default=1,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_working = models.BooleanField(
        default=True,
    )

    response_time = models.FloatField(
        default=0,
    )

    last_status_code = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    last_checked = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["priority"]
        verbose_name = "Stream"
        verbose_name_plural = "Streams"

    def __str__(self):
        return f"{self.channel.name} - {self.name}"