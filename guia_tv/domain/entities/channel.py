from dataclasses import dataclass


@dataclass(slots=True)
class Channel:

    id: int

    name: str

    slug: str

    description: str

    stream_url: str

    website: str

    logo: str | None

    country: str | None

    language: str | None

    category: str | None

    quality: str

    status: str

    is_active: bool

    is_public: bool

    is_featured: bool

    views: int

    watching_now: int

    license_status: str

    license_note: str