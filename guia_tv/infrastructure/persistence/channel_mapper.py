from guia_tv.models import Category, Channel, Country, Language


class ChannelMapper:
    """
    Traduce datos "crudos" (de un ParsedChannel de una lista M3U, o de un
    formulario de alta manual) al modelo ORM Channel, resolviendo o
    creando sus relaciones. Mantiene ese detalle de persistencia fuera de
    los casos de uso de application/.
    """

    @staticmethod
    def resolve_country(raw_name: str) -> Country | None:
        if not raw_name:
            return None

        iso = (raw_name[:2] or "XX").upper()

        country, _ = Country.objects.get_or_create(
            iso_code=iso,
            defaults={"name": raw_name},
        )
        return country

    @staticmethod
    def resolve_language(raw_name: str) -> Language:
        code = (raw_name or "es").lower()[:10]

        language, _ = Language.objects.get_or_create(
            code=code,
            defaults={"name": raw_name or "Español"},
        )
        return language

    @staticmethod
    def resolve_category(raw_name: str) -> Category:
        category, _ = Category.objects.get_or_create(
            name=raw_name or "General"
        )
        return category

    @classmethod
    def upsert_from_parsed(cls, parsed, source) -> tuple[Channel, bool]:
        """
        Crea o actualiza un Channel a partir de un ParsedChannel.

        Antes (services/import_service.py) el match era solo por `name`
        global -> si dos fuentes distintas tenían un canal con el mismo
        nombre, una pisaba a la otra. Acá el canal queda identificado por
        (source, tvg_id o nombre), así cada fuente maneja su propio set
        de canales sin chocar con otras.

        El canal hereda el license_status/license_note de la fuente: si
        la fuente no está aprobada, ImportPlaylistUseCase ni siquiera
        llega a llamar a este método (ver LicensePolicy).
        """
        country = cls.resolve_country(parsed.country)
        language = cls.resolve_language(parsed.language)
        category = cls.resolve_category(parsed.category)

        channel, created = Channel.objects.update_or_create(
            source=source,
            tvg_id=parsed.tvg_id or parsed.name,
            defaults={
                "name": parsed.name,
                "stream_url": parsed.url,
                "logo_url": parsed.logo,
                "country": country,
                "language": language,
                "category": category,
                "is_active": True,
                "status": "checking",
                "license_status": source.license_status,
                "license_note": (
                    f"Heredado de la fuente IPTV '{source.name}'."
                ),
            },
        )
        return channel, created
