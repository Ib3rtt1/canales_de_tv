from django.db import models


class Country(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    iso_code = models.CharField(
        max_length=2,
        unique=True
    )

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