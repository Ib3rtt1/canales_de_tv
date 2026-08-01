from guia_tv.infrastructure.network.http_client import HttpClient


class M3UDownloader:
    """Descarga el contenido crudo de una lista M3U remota."""

    @staticmethod
    def download(url: str) -> str:
        return HttpClient.get_text(url)
