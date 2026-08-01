# DEPRECADO: reemplazado por
# guia_tv.application.use_cases.import_playlist.SyncAllSourcesUseCase
# (respeta license_status; este archivo no lo hacía). Se deja sin borrar
# por si algo externo todavía lo importa, pero dashboard_views.py y
# management/commands/sync_iptv.py ya NO lo usan. Se puede eliminar una
# vez confirmado que nada más lo referencia.

import logging

from guia_tv.models import IPTVSource

from guia_tv.services.playlist_service import PlaylistService
from guia_tv.services.import_service import ImportService

logger = logging.getLogger(__name__)


class SyncService:

    @staticmethod
    def sync():

        total = 0

        for source in IPTVSource.objects.filter(enabled=True):

            try:
                # Antes: PlaylistService.download(source.url) -> fallaba
                # siempre porque download() espera el objeto "source", no
                # solo su url, y es un método de instancia usado como
                # si fuera estático.
                playlist = PlaylistService.download(source)

                imported = ImportService.import_playlist(playlist)

                source.total_channels = imported
                source.mark_updated()  # guarda last_update
                source.save()          # guarda total_channels

                total += imported

            except Exception:
                # Antes: print(e) -> no queda registrado en producción
                logger.exception(
                    "Error sincronizando la fuente IPTV '%s'", source.name
                )

        return total
