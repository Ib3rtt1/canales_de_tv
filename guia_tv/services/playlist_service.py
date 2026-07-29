import requests


class PlaylistService:
    """Descarga el contenido de una lista M3U desde una fuente IPTV."""

    @staticmethod
    def download(source):
        """
        source: instancia de IPTVSource (debe tener el atributo .url)
        """
        response = requests.get(source.url, timeout=60)
        response.raise_for_status()
        return response.text
