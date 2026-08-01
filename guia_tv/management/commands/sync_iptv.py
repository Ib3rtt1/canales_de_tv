from django.core.management.base import BaseCommand

from guia_tv.application.use_cases.import_playlist import SyncAllSourcesUseCase


class Command(BaseCommand):

    help = (
        "Sincroniza todas las fuentes IPTV habilitadas y con licencia "
        "aprobada (official/public_domain). Pensado para correr por cron. "
        "Reemplaza a services/sync_service.py::SyncService.sync()."
    )

    def handle(self, *args, **options):

        results = SyncAllSourcesUseCase().execute()
        total = SyncAllSourcesUseCase.total_imported(results)

        for result in results:
            if result.ok:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  {result.source_name}: {result.imported} canales"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"  {result.source_name}: omitida ({result.error})"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(f"Total sincronizado: {total} canales.")
        )
