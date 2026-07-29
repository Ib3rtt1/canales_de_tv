from django.core.management.base import BaseCommand, CommandError

from guia_tv.services.import_service import ImportService


class Command(BaseCommand):

    help = "Importar lista M3U desde un archivo local"

    def add_arguments(self, parser):
        parser.add_argument("archivo", type=str)

    def handle(self, *args, **options):

        archivo = options["archivo"]

        # Antes: este comando reimplementaba (peor) el mismo parseo
        # que ya existe en parsers/m3u_parser.py + services/import_service.py
        try:
            with open(archivo, encoding="utf-8") as f:
                contenido = f.read()
        except OSError as exc:
            raise CommandError(f"No se pudo leer el archivo: {exc}")

        total = ImportService.import_playlist(contenido)

        self.stdout.write(
            self.style.SUCCESS(f"Importación terminada: {total} canales.")
        )
