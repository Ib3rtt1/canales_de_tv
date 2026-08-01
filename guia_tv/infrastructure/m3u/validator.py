from dataclasses import dataclass

from guia_tv.infrastructure.network.http_client import HttpClient


@dataclass
class StreamCheckResult:
    is_reachable: bool
    status_code: int | None = None
    error: str = ""


class M3UValidator:
    """
    Chequeo liviano (HEAD, sin descargar el video) de si una URL de
    stream responde. Se usa al importar/agregar un canal para no guardar
    URLs claramente muertas. No reemplaza un monitoreo periódico de
    salud -- eso necesitaría un job aparte que recorra los canales ya
    guardados.
    """

    @staticmethod
    def check(url: str) -> StreamCheckResult:
        try:
            response = HttpClient.head(url)
            return StreamCheckResult(
                is_reachable=response.status_code < 400,
                status_code=response.status_code,
            )
        except Exception as exc:
            return StreamCheckResult(is_reachable=False, error=str(exc))
