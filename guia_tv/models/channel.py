from django.db import models
from django.utils.text import slugify

from .category import Category
from .country import Country
from .language import Language


class Channel(models.Model):

    QUALITY_CHOICES = [
        ("SD", "SD"),
        ("HD", "HD"),
        ("FHD", "Full HD"),
        ("4K", "4K"),
    ]

    STATUS_CHOICES = [
        ("checking", "Verificando"),
        ("online", "Online"),
        ("offline", "Offline"),
    ]

    name = models.CharField(max_length=200)

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    stream_url = models.URLField(
        max_length=1000
    )

    website = models.URLField(
        blank=True
    )

    logo = models.ImageField(
        upload_to="channels/logos/",
        blank=True,
        null=True
    )

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

    quality = models.CharField(
        max_length=10,
        choices=QUALITY_CHOICES,
        default="HD"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="checking"
    )

    epg_id = models.CharField(
        max_length=200,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    is_public = models.BooleanField(
        default=True
    )

    is_featured = models.BooleanField(
        default=False
    )

    views = models.PositiveIntegerField(
        default=0
    )

    watching_now = models.PositiveIntegerField(
        default=0
    )

    last_checked = models.DateTimeField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Canal"
        verbose_name_plural = "Canales"

        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["is_featured"]),
            models.Index(fields=["country"]),
            models.Index(fields=["category"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            # Antes: self.slug = slugify(self.name) sin más -> si dos
            # canales generaban el mismo slug, el segundo save()
            # lanzaba IntegrityError (slug es unique).
            base_slug = slugify(self.name)
            slug = base_slug
            contador = 1

            while (
                Channel.objects
                .filter(slug=slug)
                .exclude(pk=self.pk)
                .exists()
            ):
                contador += 1
                slug = f"{base_slug}-{contador}"

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
