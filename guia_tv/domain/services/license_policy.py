from guia_tv.domain.value_objects.license_status import LicenseStatus


class LicensePolicyError(Exception):
    """La operación pedida viola la política de licencias del proyecto."""


class LicensePolicy:
    """
    Reglas de negocio sobre derechos de autor. Toda importación o alta de
    canal DEBE pasar por acá antes de tocar la base de datos.

    Principio: una fuente o canal nunca se sincroniza/publica solo por
    estar "enabled" o "is_active" -- además necesita licencia aprobada
    (OFFICIAL o PUBLIC_DOMAIN), revisada por una persona.
    """

    @staticmethod
    def assert_source_syncable(source) -> None:
        if not source.enabled:
            raise LicensePolicyError(
                f"La fuente '{source.name}' está deshabilitada."
            )

        status = LicenseStatus(source.license_status)

        if not status.is_publishable:
            raise LicensePolicyError(
                f"La fuente '{source.name}' tiene licencia '{status.value}' "
                "y no puede sincronizarse automáticamente. Marcala como "
                "'official' o 'public_domain' recién después de confirmar "
                "que el canal autoriza ese stream, o 'rejected' si no."
            )

    @staticmethod
    def assert_channel_publishable(license_status: str, license_note: str) -> None:
        status = LicenseStatus(license_status)

        if not status.is_publishable:
            raise LicensePolicyError(
                "Solo se pueden publicar canales con licencia 'official' o "
                "'public_domain'. Si no estás seguro del origen, guardalo "
                "como 'pending' y no lo actives todavía."
            )

        if not license_note or not license_note.strip():
            raise LicensePolicyError(
                "Falta la nota de licencia: explicá de dónde sale la "
                "autorización para transmitir este canal (ej. 'stream "
                "oficial embebible publicado en el sitio del canal')."
            )
