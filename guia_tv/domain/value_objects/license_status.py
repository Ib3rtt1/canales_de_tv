from enum import Enum


class LicenseStatus(str, Enum):
    """
    Estado de licencia de un canal o de una fuente IPTV.

    - PENDING: recién agregado, sin revisión humana todavía. NUNCA debe
      sincronizarse ni mostrarse públicamente en este estado.
    - OFFICIAL: el propio canal/organismo publica ese stream para
      consumo público (ej. TV pública, canal de gobierno, universidad).
    - PUBLIC_DOMAIN: contenido en dominio público o con licencia abierta
      (Creative Commons u equivalente).
    - REJECTED: fue revisado y descartado por posibles derechos de autor.
      Queda registrado para no volver a intentarlo por error.
    """

    PENDING = "pending"
    OFFICIAL = "official"
    PUBLIC_DOMAIN = "public_domain"
    REJECTED = "rejected"

    @property
    def is_publishable(self) -> bool:
        """¿Se puede sincronizar/mostrar públicamente en este estado?"""
        return self in (LicenseStatus.OFFICIAL, LicenseStatus.PUBLIC_DOMAIN)

    @classmethod
    def choices(cls):
        """Formato (value, label) listo para usar como Django choices."""
        labels = {
            cls.PENDING: "Pendiente de revisión",
            cls.OFFICIAL: "Oficial del canal/organismo",
            cls.PUBLIC_DOMAIN: "Dominio público / licencia abierta",
            cls.REJECTED: "Rechazado (posibles derechos de autor)",
        }
        return [(status.value, labels[status]) for status in cls]
