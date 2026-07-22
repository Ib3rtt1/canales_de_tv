#import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Country(models.Model):

    name = models.CharField(max_length=100, unique=True)

    iso_code = models.CharField(max_length=2, unique=True)

    flag = models.ImageField(
        upload_to="flags/",
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "País"
        verbose_name_plural = "Países"

    def __str__(self):
        return self.name


class Language(models.Model):

    name = models.CharField(max_length=100)

    code = models.CharField(max_length=10)

    class Meta:
        ordering = ["name"]
        verbose_name = "Idioma"
        verbose_name_plural = "Idiomas"

    def __str__(self):
        return self.name


class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    icon = models.CharField(
        max_length=100,
        blank=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.name


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
        null=True,
        blank=True
    )

    language = models.ForeignKey(
        Language,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]
        verbose_name = "Canal"
        verbose_name_plural = "Canales"

    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


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


class Favorite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("user", "channel")
        verbose_name = "Favorito"
        verbose_name_plural = "Favoritos"

    def __str__(self):
        return f"{self.user.username} - {self.channel.name}"


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