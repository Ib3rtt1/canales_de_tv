import time

import requests
from django.core.management.base import BaseCommand
from django.utils import timezone

from guia_tv.models import ChannelStream


class Command(BaseCommand):
    help = "Verifica la disponibilidad de los streams de video activos"

    def handle(self, *args, **options):
        self.stdout.write("Iniciando verificación de transmisiones...")

        # Antes: el comando calculaba is_online pero comprobaba
        # hasattr(stream, 'is_online') / hasattr(stream, 'status'), que
        # ChannelStream NO tiene (tiene is_working/last_status_code/
        # response_time/last_checked) -> nunca guardaba nada, el comando
        # corría "exitosamente" sin actualizar un solo registro.
        streams = ChannelStream.objects.filter(is_active=True)

        total = streams.count()
        online_count = 0

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        for index, stream in enumerate(streams, start=1):
            channel_name = f"{stream.channel.name} - {stream.name}"

            self.stdout.write(f"[{index}/{total}] Verificando {channel_name}...")

            status_code = None
            started = time.monotonic()

            try:
                response = requests.head(
                    stream.url, headers=headers, timeout=5, allow_redirects=True
                )

                if response.status_code >= 400:
                    response = requests.get(
                        stream.url, headers=headers, timeout=5, stream=True
                    )

                status_code = response.status_code
                is_online = status_code < 400

            except requests.RequestException:
                is_online = False

            stream.is_working = is_online
            stream.last_status_code = status_code
            stream.response_time = round(time.monotonic() - started, 3)
            stream.last_checked = timezone.now()

            stream.save(
                update_fields=[
                    "is_working",
                    "last_status_code",
                    "response_time",
                    "last_checked",
                ]
            )

            if is_online:
                online_count += 1
                self.stdout.write(self.style.SUCCESS(f"   [OK] {channel_name} en línea"))
            else:
                self.stdout.write(
                    self.style.WARNING(f"   [OFFLINE] {channel_name} no responde")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nVerificación finalizada: {online_count}/{total} streams disponibles."
            )
        )