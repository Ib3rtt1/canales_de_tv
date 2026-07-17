from django.contrib import admin

from .models import (
    Category,
    Channel,
    Country,
    Language,
    IPTVSource,
)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "iso_code")
    search_fields = ("name",)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "country",
        "category",
        "language",
        "is_active",
        "views",
    )

    list_filter = (
        "country",
        "category",
        "language",
        "is_active",
    )

    search_fields = (
        "name",
        "description",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


@admin.register(IPTVSource)
class IPTVSourceAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "enabled",
        "last_update",
    )

    search_fields = (
        "name",
        "url",
    )