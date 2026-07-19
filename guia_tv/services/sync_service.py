from guia_tv.models import IPTVSource

from guia_tv.services.playlist_service import PlaylistService
from guia_tv.services.import_service import ImportService


class SyncService:

    @staticmethod
    def sync():

        total = 0

        for source in IPTVSource.objects.filter(enabled=True):

            try:

                playlist = PlaylistService.download(
                    source.url
                )

                imported = ImportService.import_playlist(
                    playlist
                )

                source.total_channels = imported

                source.mark_updated()

                source.save()

                total += imported

            except Exception as e:

                print(e)

        return total