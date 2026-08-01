import requests
from django.core.management.base import BaseCommand
from guia_tv.models import ChannelStream

class Command(BaseCommand):
    help = 'Verifica la disponibilidad de los streams de video activos'

    def handle(self, *args, **options):
        self.stdout.write("Iniciando verificación de transmisiones...")

        # Filtra si existe is_active, de lo contrario trae todos
        streams = ChannelStream.objects.all()
        if hasattr(ChannelStream, 'is_active'):
            streams = streams.filter(is_active=True)

        total = streams.count()
        online_count = 0

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        for index, stream in enumerate(streams, start=1):
            url = getattr(stream, 'url', None) or getattr(stream, 'stream_url', '')
            channel_name = getattr(stream, 'name', f"Stream #{stream.pk}")
            
            if not url:
                continue

            self.stdout.write(f"[{index}/{total}] Verificando {channel_name}...")

            try:
                # Comprobación rápida por HTTP HEAD / GET
                response = requests.head(url, headers=headers, timeout=5, allow_redirects=True)
                if response.status_code >= 400:
                    response = requests.get(url, headers=headers, timeout=5, stream=True)

                is_online = response.status_code < 400

            except Exception:
                is_online = False

            if hasattr(stream, 'is_online'):
                stream.is_online = is_online
            elif hasattr(stream, 'status'):
                stream.status = 'online' if is_online else 'offline'

            stream.save()

            if is_online:
                online_count += 1
                self.stdout.write(self.style.SUCCESS(f"   [OK] {channel_name} en línea"))
            else:
                self.stdout.write(self.style.WARNING(f"   [OFFLINE] {channel_name} no responde"))

        self.stdout.write(self.style.SUCCESS(f"\nVerificación finalizada: {online_count}/{total} canales disponibles."))