# DEPRECADO: reemplazado por
# guia_tv.infrastructure.persistence.channel_mapper.ChannelMapper
# + guia_tv.application.use_cases.import_playlist.ImportPlaylistUseCase.
# Este servicio matcheaba canales solo por `name` global (colisiona entre
# fuentes distintas) y no aplicaba ninguna política de licencias.

from guia_tv.models import (
    Category,
    Channel,
    Country,
    Language,
)

from guia_tv.parsers.m3u_parser import M3UParser

class ImportService:

    @staticmethod
    def import_playlist(content):

        channels = M3UParser.parse(content)

        imported = 0

        for item in channels:

            country, _ = Country.objects.get_or_create(
                iso_code=(item["country"][:2] or "XX").upper(),
                defaults={
                    "name": item["country"] or "Desconocido"
                }
            )

            language, _ = Language.objects.get_or_create(
                code=(item["language"] or "es").lower(),
                defaults={
                    "name": item["language"] or "Español"
                }
            )

            category, _ = Category.objects.get_or_create(
                name=item["category"] or "General"
            )

            Channel.objects.update_or_create(

                name=item["name"],

                defaults={
                    "country": country,
                    "language": language,
                    "category": category,
                    "stream_url": item["url"],
                    "is_active": True,
                }

            )

            imported += 1

        return imported