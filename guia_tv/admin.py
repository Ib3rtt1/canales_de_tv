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
        "country",
        "category",
        "quality",
        "status",
        "views",
        "is_active",
        "is_featured",
    )

    list_filter = (
        "country",
        "category",
        "quality",
        "status",
        "is_active",
        "is_featured",
    )

    search_fields = (
        "name",
        "description",
        "epg_id",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    list_per_page = 50


@admin.register(IPTVSource)
class IPTVSourceAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "enabled",
        "priority",
        "total_channels",
        "last_update",
    )

    list_filter = (
        "enabled",
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