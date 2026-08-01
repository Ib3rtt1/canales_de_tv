from django.core.management.base import BaseCommand, CommandError

from guia_tv.domain.value_objects.license_status import LicenseStatus
from guia_tv.infrastructure.m3u.parser import M3UParser
from guia_tv.infrastructure.persistence.channel_mapper import ChannelMapper
from guia_tv.models import IPTVSource


class Command(BaseCommand):

    help = (
        "Importar una lista M3U desde un archivo local. Requiere declarar "
        "el estado de licencia de esa lista (no se importa nada sin esto)."
    )

    def add_arguments(self, parser):
        parser.add_argument("archivo", type=str)

        parser.add_argument(
            "--license",
            required=True,
            choices=["official", "public_domain"],
            help=(
                "Estado de licencia que se le asigna a TODOS los canales "
                "de este archivo. Usá 'official' si la lista viene "
                "directamente del canal/organismo, o 'public_domain' si "
                "es contenido de licencia abierta."
            ),
        )

        parser.add_argument(
            "--source-name",
            default=None,
            help="Nombre a usar para agrupar esta importación (por defecto, el nombre del archivo).",
        )

        parser.add_argument(
            "--note",
            default="",
            help="Justificación de la licencia (recomendado).",
        )

    def handle(self, *args, **options):

        archivo = options["archivo"]
        license_status = options["license"]
        note = options["note"]
        source_name = options["source_name"] or f"Archivo local: {archivo}"

        try:
            with open(archivo, encoding="utf-8") as f:
                contenido = f.read()
        except OSError as exc:
            raise CommandError(f"No se pudo leer el archivo: {exc}")

        # Cada importación local queda asociada a una IPTVSource "de
        # archivo" (url ficticia, enabled=False para que nunca la toque
        # el sync automático), así los canales quedan agrupados y
        # trazables igual que los que vienen de una fuente remota.
        source, _ = IPTVSource.objects.get_or_create(
            name=source_name,
            defaults={
                "url": f"file://{archivo}",
                "enabled": False,
                "auto_update": False,
            },
        )

        source.license_status = license_status
        source.license_note = note or source.license_note
        source.save(update_fields=["license_status", "license_note"])

        parsed_channels = M3UParser.parse(contenido)

        importados = 0

        for parsed in parsed_channels:
            if not parsed.url:
                continue
            ChannelMapper.upsert_from_parsed(parsed, source)
            importados += 1

        source.total_channels = importados
        source.mark_updated()
        source.save(update_fields=["total_channels"])

        estado = LicenseStatus(license_status)

        self.stdout.write(
            self.style.SUCCESS(
                f"Importación terminada: {importados} canales "
                f"(licencia: {estado.value})."
            )
        )
