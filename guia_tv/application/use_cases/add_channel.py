from dataclasses import dataclass

from guia_tv.domain.services.license_policy import (
    LicensePolicy,
    LicensePolicyError,
)
from guia_tv.infrastructure.m3u.validator import M3UValidator
from guia_tv.repositories.channel_repository import ChannelRepository


@dataclass
class AddChannelInput:
    name: str
    stream_url: str
    license_status: str        # 'official' | 'public_domain' (obligatorio)
    license_note: str          # de dónde sale la autorización
    website: str = ""
    logo_url: str = ""
    country_id: int | None = None
    language_id: int | None = None
    category_id: int | None = None
    quality: str = "HD"
    skip_url_check: bool = False


class AddChannelError(Exception):
    pass


class AddChannelUseCase:
    """
    Alta manual de UN canal (no viene de una lista M3U masiva).

    Reglas que aplica antes de guardar nada:
    1. LicensePolicy: el estado de licencia debe ser 'official' o
       'public_domain', y tiene que venir con una nota explicando el
       origen -- no se puede publicar un canal "porque sí".
    2. No se permite duplicar la misma stream_url dos veces.
    3. (Opcional) Verifica que la URL responda antes de guardar, para no
       publicar un stream muerto desde el primer momento.
    """

    def execute(self, data: AddChannelInput):
        try:
            LicensePolicy.assert_channel_publishable(
                data.license_status, data.license_note
            )
        except LicensePolicyError as exc:
            raise AddChannelError(str(exc)) from exc

        if not data.name.strip():
            raise AddChannelError("El canal necesita un nombre.")

        if ChannelRepository.exists_with_url(data.stream_url):
            raise AddChannelError(
                "Ya existe un canal con esa misma URL de stream."
            )

        if not data.skip_url_check:
            check = M3UValidator.check(data.stream_url)
            if not check.is_reachable:
                raise AddChannelError(
                    "La URL del stream no respondió correctamente "
                    f"({check.error or check.status_code}). Revisala antes "
                    "de guardar, o marcá 'omitir verificación' si sabés "
                    "que es un falso negativo (por ejemplo, servidores "
                    "que bloquean peticiones HEAD)."
                )

        channel = ChannelRepository.create(
            name=data.name.strip(),
            stream_url=data.stream_url,
            website=data.website,
            logo_url=data.logo_url,
            quality=data.quality,
            country_id=data.country_id,
            language_id=data.language_id,
            category_id=data.category_id,
            is_active=True,
            status="checking",
            license_status=data.license_status,
            license_note=data.license_note.strip(),
        )

        return channel
