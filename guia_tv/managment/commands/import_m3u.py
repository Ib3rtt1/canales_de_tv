import re

from django.core.management.base import BaseCommand

from guia_tv.models import (
    Category,
    Channel,
    Country,
    Language,
)


class Command(BaseCommand):

    help = "Importar lista M3U"

    def add_arguments(self, parser):
        parser.add_argument("archivo", type=str)

    def handle(self, *args, **options):

        archivo = options["archivo"]

        with open(archivo, encoding="utf-8") as f:
            lineas = f.readlines()

        canal = {}

        for linea in lineas:

            linea = linea.strip()

            if linea.startswith("#EXTINF"):

                canal = {}

                def buscar(campo):
                    r = re.search(fr'{campo}="([^"]*)"', linea)
                    return r.group(1) if r else ""

                canal["nombre"] = linea.split(",")[-1]

                canal["logo"] = buscar("tvg-logo")

                canal["pais"] = buscar("tvg-country")

                canal["categoria"] = buscar("group-title")

                canal["idioma"] = buscar("tvg-language")

            elif linea.startswith("http"):

                canal["url"] = linea

                country, _ = Country.objects.get_or_create(
                    iso_code=canal["pais"][:2].upper() or "XX",
                    defaults={
                        "name": canal["pais"] or "Desconocido"
                    }
                )

                language, _ = Language.objects.get_or_create(
                    code=(canal["idioma"] or "es").lower(),
                    defaults={
                        "name": canal["idioma"] or "Español"
                    }
                )

                category, _ = Category.objects.get_or_create(
                    name=canal["categoria"] or "General"
                )

                Channel.objects.update_or_create(

                    name=canal["nombre"],

                    defaults={

                        "stream_url": canal["url"],

                        "website": "",

                        "description": "",

                        "country": country,

                        "language": language,

                        "category": category,

                        "is_active": True,

                    }

                )

        self.stdout.write(
            self.style.SUCCESS("Importación terminada")
        )