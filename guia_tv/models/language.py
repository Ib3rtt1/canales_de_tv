from django.db import models


class Language(models.Model):

    name = models.CharField(
        max_length=100
    )

    code = models.CharField(
        max_length=10
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Idioma"
        verbose_name_plural = "Idiomas"

    def __str__(self):
        return self.name