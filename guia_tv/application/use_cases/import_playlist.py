import logging
from dataclasses import dataclass

from guia_tv.domain.services.license_policy import (
    LicensePolicy,
    LicensePolicyError,
)
from guia_tv.infrastructure.m3u.downloader import M3UDownloader
from guia_tv.infrastructure.m3u.parser import M3UParser
from guia_tv.infrastructure.persistence.channel_mapper import ChannelMapper
from guia_tv.repositories.iptv_source_repository import IPTVSourceRepository

logger = logging.getLogger(__name__)


@dataclass
class ImportPlaylistResult:
    source_name: str
    imported: int = 0
    skipped: int = 0
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None


class ImportPlaylistUseCase:
    """
    Caso de uso: importar los canales de UNA fuente IPTV.

    Antes de tocar la red, valida con LicensePolicy que la fuente esté
    habilitada Y con licencia aprobada (official/public_domain). Si está
    "pending" o "rejected", no se descarga absolutamente nada -- así una
    fuente recién agregada nunca se sincroniza sin revisión humana.
    """

    def execute(self, source) -> ImportPlaylistResult:
        try:
            LicensePolicy.assert_source_syncable(source)
        except LicensePolicyError as exc:
            return ImportPlaylistResult(source.name, error=str(exc))

        try:
            raw_playlist = M3UDownloader.download(source.url)
        except Exception as exc:
            logger.exception(
                "No se pudo descargar la fuente IPTV '%s'", source.name
            )
            return ImportPlaylistResult(source.name, error=str(exc))

        parsed_channels = M3UParser.parse(raw_playlist)

        imported = 0
        skipped = 0

        for parsed in parsed_channels:
            if not parsed.url:
                skipped += 1
                continue

            ChannelMapper.upsert_from_parsed(parsed, source)
            imported += 1

        source.total_channels = imported
        source.mark_updated()
        source.save(update_fields=["total_channels"])

        return ImportPlaylistResult(source.name, imported=imported, skipped=skipped)


class SyncAllSourcesUseCase:
    """
    Recorre todas las fuentes sincronizables (enabled + licencia
    aprobada) y ejecuta ImportPlaylistUseCase sobre cada una. Reemplaza a
    services/sync_service.py::SyncService.sync().
    """

    def __init__(self, import_use_case: ImportPlaylistUseCase | None = None):
        self._import_use_case = import_use_case or ImportPlaylistUseCase()

    def execute(self) -> list[ImportPlaylistResult]:
        results = []

        for source in IPTVSourceRepository.syncable():
            result = self._import_use_case.execute(source)
            results.append(result)

            if not result.ok:
                logger.warning(
                    "Fuente '%s' omitida: %s", source.name, result.error
                )

        return results

    @staticmethod
    def total_imported(results: list[ImportPlaylistResult]) -> int:
        return sum(r.imported for r in results if r.ok)
