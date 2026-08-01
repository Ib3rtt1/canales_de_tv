import re
from dataclasses import dataclass


@dataclass
class ParsedChannel:
    """Un canal tal como sale de una lista M3U, sin tocar todavía la base."""

    name: str
    url: str = ""
    logo: str = ""
    country: str = ""
    language: str = ""
    category: str = ""
    tvg_id: str = ""
    tvg_name: str = ""


class M3UParser:
    """
    Parser de listas M3U/M3U8 extendidas (#EXTM3U + #EXTINF).

    Mejoras respecto al parser anterior (guia_tv/parsers/m3u_parser.py):
    - El nombre del canal es todo lo que sigue a la ÚLTIMA coma de la
      línea #EXTINF (así lo define el estándar). Antes se usaba
      line.split(",")[-1], que en la práctica da el mismo resultado para
      el caso simple pero no filtraba nombres vacíos ni bytes BOM.
    - Ignora explícitamente #EXTGRP, #EXTVLCOPT y cualquier otra línea
      de comentario (#...) que no sea #EXTINF, en vez de simplemente no
      contemplarlas.
    - Tolera BOM al inicio de línea y líneas en blanco.
    - Si la lista viene cortada (un #EXTINF sin URL después), ese bloque
      se descarta en vez de arrastrar datos del canal anterior.
    """

    _ATTR_RE = re.compile(r'([\w-]+)="([^"]*)"')

    @classmethod
    def parse(cls, content: str) -> list[ParsedChannel]:
        channels: list[ParsedChannel] = []
        pending: dict | None = None

        for raw_line in (content or "").splitlines():
            line = raw_line.strip().lstrip("\ufeff")

            if not line:
                continue

            if line.startswith("#EXTINF"):
                pending = cls._parse_extinf(line)
                continue

            if line.startswith("#"):
                # #EXTGRP, #EXTVLCOPT, comentarios sueltos -> se ignoran
                continue

            if pending is not None:
                pending["url"] = line
                channels.append(ParsedChannel(**pending))
                pending = None

        return channels

    @classmethod
    def _parse_extinf(cls, line: str) -> dict:
        attrs = dict(cls._ATTR_RE.findall(line))

        name = line.rsplit(",", 1)[-1].strip() if "," in line else ""

        return {
            "name": name or "Sin nombre",
            "logo": attrs.get("tvg-logo", ""),
            "country": attrs.get("tvg-country", ""),
            "language": attrs.get("tvg-language", ""),
            "category": attrs.get("group-title", ""),
            "tvg_id": attrs.get("tvg-id", ""),
            "tvg_name": attrs.get("tvg-name", ""),
        }
