from guia_tv.models import IPTVSource


class IPTVSourceRepository:

    @staticmethod
    def all():
        return IPTVSource.objects.all()

    @staticmethod
    def enabled():
        return IPTVSource.objects.filter(enabled=True)

    @staticmethod
    def syncable():
        """Fuentes habilitadas Y con licencia ya aprobada."""
        return IPTVSource.objects.filter(
            enabled=True,
            license_status__in=["official", "public_domain"],
        )

    @staticmethod
    def pending_review():
        """Fuentes nuevas que un humano todavía no revisó."""
        return IPTVSource.objects.filter(license_status="pending")

    @staticmethod
    def by_id(source_id):
        return IPTVSource.objects.filter(pk=source_id).first()
