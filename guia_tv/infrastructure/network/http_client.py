import requests


class HttpClient:
    """
    Cliente HTTP delgado. El resto de la app (application/, domain/) no
    debería importar `requests` directamente: siempre pasa por acá, para
    poder cambiar de librería o agregar reintentos/caché en un solo lugar.
    """

    DEFAULT_TIMEOUT = 20
    USER_AGENT = "guia-tv-importer/1.0 (+revision manual de licencias)"

    @classmethod
    def get_text(cls, url: str, timeout: int | None = None) -> str:
        response = requests.get(
            url,
            timeout=timeout or cls.DEFAULT_TIMEOUT,
            headers={"User-Agent": cls.USER_AGENT},
        )
        response.raise_for_status()
        return response.text

    @classmethod
    def head(cls, url: str, timeout: int = 8):
        return requests.head(
            url,
            timeout=timeout,
            headers={"User-Agent": cls.USER_AGENT},
            allow_redirects=True,
        )
