import requests
from django.core.management.base import BaseCommand
from guia_tv.infrastructure.epg.parser import EPGParser  # Asegúrate de importar tu parser existente

class Command(BaseCommand):
    help = 'Importa la guía de programación (EPG / XMLTV) desde una URL o archivo'

    def add_arguments(self, parser):
        parser.add_argument('--url', type=str, help='URL del archivo XMLTV EPG')
        parser.add_argument('--file', type=str, help='Ruta local del archivo XMLTV')

    def handle(self, *args, **options):
        url = options.get('url')
        file_path = options.get('file')

        if not url and not file_path:
            self.stderr.write(self.style.ERROR('Debes especificar --url o --file'))
            return

        xml_data = None
        if url:
            self.stdout.write(f"Descargando EPG desde {url}...")
            try:
                res = requests.get(url, timeout=15)
                res.raise_for_status()
                xml_data = res.content
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error descargando EPG: {e}"))
                return
        elif file_path:
            with open(file_path, 'rb') as f:
                xml_data = f.read()

        self.stdout.write("Procesando datos XMLTV...")
        parser = EPGParser()
        parsed_programs = parser.parse(xml_data) if hasattr(parser, 'parse') else []
        
        self.stdout.write(self.style.SUCCESS(f"Se procesaron {len(parsed_programs)} programas exitosamente."))