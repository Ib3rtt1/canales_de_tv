from django.db import models
from django.utils import timezone

from guia_tv.domain.value_objects.license_status import LicenseStatus


class IPTVSource(models.Model):

    LICENSE_CHOICES = LicenseStatus.choices()

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

    # ==========================================
    # DERECHOS / LICENCIA
    # ==========================================

    license_status = models.CharField(
        max_length=20,
        choices=LICENSE_CHOICES,
        default=LicenseStatus.PENDING.value,
        help_text=(
            "Una fuente nueva arranca en 'pending' y NO se sincroniza "
            "automáticamente hasta que alguien confirme que sus canales "
            "están autorizados (official/public_domain)."
        ),
    )

    license_note = models.TextField(
        blank=True,
        help_text="Justificación de por qué esta fuente es confiable.",
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
