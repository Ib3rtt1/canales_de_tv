from django.db import models
from django.utils.text import slugify

from guia_tv.domain.value_objects.license_status import LicenseStatus

from .category import Category
from .country import Country
from .language import Language


class Channel(models.Model):

    # ==================================================
    # OPCIONES
    # ==================================================

    QUALITY_CHOICES = [
        ("SD", "SD"),
        ("HD", "HD"),
        ("FHD", "Full HD"),
        ("4K", "4K"),
    ]

    LICENSE_CHOICES = LicenseStatus.choices()

    STATUS_CHOICES = [
        ("checking", "Verificando"),
        ("online", "Online"),
        ("offline", "Offline"),
    ]

    STREAM_TYPES = [
        ("HLS", "HLS (.m3u8)"),
        ("MPD", "MPEG-DASH"),
        ("TS", "MPEG-TS"),
        ("RTMP", "RTMP"),
        ("OTHER", "Otro"),
    ]

    SOURCE_CHOICES = [
        ("iptv", "IPTV"),
        ("youtube", "YouTube"),
        ("twitch", "Twitch"),
    ]

    # ==================================================
    # INFORMACIÓN GENERAL
    # ==================================================

    name = models.CharField(max_length=200)

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    description = models.TextField(blank=True)

    website = models.URLField(blank=True)

    # ==================================================
    # ORIGEN DEL CANAL
    # ==================================================

    source_type = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default="iptv",
    )

    # ==================================================
    # IPTV
    # ==================================================

    stream_url = models.URLField(
        max_length=1000,
        blank=True,
    )

    stream_type = models.CharField(
        max_length=20,
        choices=STREAM_TYPES,
        default="HLS",
    )

    tvg_id = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
    )

    tvg_name = models.CharField(
        max_length=255,
        blank=True,
    )

    epg_id = models.CharField(
        max_length=255,
        blank=True,
    )

    # ==================================================
    # YOUTUBE
    # ==================================================

    youtube_video_id = models.CharField(
        max_length=100,
        blank=True,
    )

    youtube_channel = models.CharField(
        max_length=200,
        blank=True,
    )

    # ==================================================
    # IMÁGENES
    # ==================================================

    logo = models.ImageField(
        upload_to="channels/logos/",
        blank=True,
        null=True,
    )

    logo_url = models.URLField(blank=True)

    # ==================================================
    # RELACIONES
    # ==================================================

    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        related_name="channels",
        null=True,
        blank=True,
    )

    language = models.ForeignKey(
        Language,
        on_delete=models.SET_NULL,
        related_name="channels",
        null=True,
        blank=True,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="channels",
        null=True,
        blank=True,
    )

    # ==================================================
    # CALIDAD
    # ==================================================

    quality = models.CharField(
        max_length=10,
        choices=QUALITY_CHOICES,
        default="HD",
    )

    resolution = models.CharField(
        max_length=30,
        blank=True,
    )

    bitrate = models.PositiveIntegerField(
        default=0,
    )

    video_codec = models.CharField(
        max_length=50,
        blank=True,
    )

    audio_codec = models.CharField(
        max_length=50,
        blank=True,
    )

    # ==================================================
    # ESTADO
    # ==================================================

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="checking",
    )

    is_verified = models.BooleanField(default=False)

    last_status_code = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    response_time = models.FloatField(default=0)

    last_checked = models.DateTimeField(
        blank=True,
        null=True,
    )

    # ==================================================
    # LICENCIA
    # ==================================================

    license_status = models.CharField(
        max_length=20,
        choices=LICENSE_CHOICES,
        default=LicenseStatus.PENDING.value,
    )

    license_note = models.TextField(blank=True)

    # ==================================================
    # VISIBILIDAD
    # ==================================================

    is_active = models.BooleanField(default=True)

    is_public = models.BooleanField(default=True)

    is_featured = models.BooleanField(default=False)

    # ==================================================
    # ESTADÍSTICAS
    # ==================================================

    views = models.PositiveIntegerField(default=0)

    watching_now = models.PositiveIntegerField(default=0)

    # ==================================================
    # FECHAS
    # ==================================================

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    # ==================================================
    # META
    # ==================================================

    class Meta:

        ordering = ["name"]

        verbose_name = "Canal"

        verbose_name_plural = "Canales"

        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["country"]),
            models.Index(fields=["category"]),
            models.Index(fields=["language"]),
            models.Index(fields=["status"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["is_featured"]),
            models.Index(fields=["tvg_id"]),
            models.Index(fields=["license_status"]),
        ]

    # ==================================================
    # SAVE
    # ==================================================

    def save(self, *args, **kwargs):

        if not self.slug:

            base_slug = slugify(self.name)

            slug = base_slug

            contador = 2

            while Channel.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{contador}"
                contador += 1

            self.slug = slug

        super().save(*args, **kwargs)

    # ==================================================
    # HELPERS
    # ==================================================

    @property
    def is_youtube(self):
        return self.source_type == "youtube"

    @property
    def is_iptv(self):
        return self.source_type == "iptv"

    @property
    def is_twitch(self):
        return self.source_type == "twitch"

    # ==================================================
    # STR
    # ==================================================

    def __str__(self):
        return self.name