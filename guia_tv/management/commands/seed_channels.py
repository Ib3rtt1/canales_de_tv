import json
from pathlib import Path

from django.core.management.base import BaseCommand

from guia_tv.models import (
    Category,
    Channel,
    Country,
    Language,
)


class Command(BaseCommand):

    help = "Carga canales iniciales"

    def handle(self, *args, **kwargs):

        archivo = (
            Path(__file__)
            .resolve()
            .parents[2]
            / "fixtures"
            / "channels.json"
        )

        with open(archivo, encoding="utf-8") as f:
            canales = json.load(f)

        total = 0

        for item in canales:

            country, _ = Country.objects.get_or_create(
                name=item["country"],
                defaults={
                    "iso_code": item["country"][:2].upper()
                }
            )

            language, _ = Language.objects.get_or_create(
                name=item["language"],
                defaults={
                    "code": item["language"][:2].lower()
                }
            )

            category, _ = Category.objects.get_or_create(
                name=item["category"]
            )

            channel, created = Channel.objects.get_or_create(
                name=item["name"],
                defaults={
                    "country": country,
                    "language": language,
                    "category": category,
                    "stream_url": item["stream"],
                    "is_featured": item["featured"],
                    "is_active": True,
                },
            )

            if created:
                total += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Se importaron {total} canales."
            )
        )