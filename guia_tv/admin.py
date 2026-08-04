from django.contrib import admin

from .models import (
    Category,
    Channel,
    Country,
    Favorite,
    IPTVSource,
    Language,
    WatchHistory,
)


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "source_type",
        "country",
        "category",
        "quality",
        "status",
        "license_status",
        "views",
        "is_active",
        "is_featured",
    )

    list_filter = (
        "source_type",
        "country",
        "category",
        "quality",
        "status",
        "license_status",
        "is_active",
        "is_featured",
    )

    search_fields = (
        "name",
        "description",
        "youtube_channel",
        "youtube_video_id",
        "epg_id",
    )

    readonly_fields = (
        "views",
        "watching_now",
        "created_at",
        "updated_at",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    fieldsets = (

        (
            "Información general",
            {
                "fields": (
                    "name",
                    "slug",
                    "description",
                    "website",
                    "logo",
                    "logo_url",
                )
            },
        ),

        (
            "Origen del canal",
            {
                "fields": (
                    "source_type",
                )
            },
        ),

        (
            "IPTV",
            {
                "fields": (
                    "stream_url",
                    "stream_type",
                    "tvg_id",
                    "tvg_name",
                    "epg_id",
                )
            },
        ),

        (
            "YouTube",
            {
                "fields": (
                    "youtube_video_id",
                    "youtube_channel",
                )
            },
        ),

        (
            "Clasificación",
            {
                "fields": (
                    "country",
                    "language",
                    "category",
                    "quality",
                    "resolution",
                )
            },
        ),

        (
            "Estado",
            {
                "fields": (
                    "status",
                    "is_verified",
                    "response_time",
                    "last_checked",
                )
            },
        ),

        (
            "Licencia",
            {
                "fields": (
                    "license_status",
                    "license_note",
                )
            },
        ),

        (
            "Visibilidad",
            {
                "fields": (
                    "is_active",
                    "is_public",
                    "is_featured",
                )
            },
        ),

        (
            "Estadísticas",
            {
                "fields": (
                    "views",
                    "watching_now",
                )
            },
        ),

        (
            "Fechas",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),

    )

    list_per_page = 50


@admin.register(IPTVSource)
class IPTVSourceAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "enabled",
        "license_status",
        "priority",
        "total_channels",
        "last_update",
    )

    list_filter = (
        "enabled",
        "license_status",
        "auto_update",
    )

    search_fields = (
        "name",
        "url",
    )


admin.site.register(Category)
admin.site.register(Country)
admin.site.register(Language)
admin.site.register(Favorite)
admin.site.register(WatchHistory)