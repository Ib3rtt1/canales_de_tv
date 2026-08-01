from django.http import JsonResponse
from guia_tv.repositories.channel_repository import ChannelRepository


def search_channels(request):

    q = request.GET.get("q", "").strip()

    # Antes: Channel.objects.filter(is_active=True, ...), sin filtrar
    # por licencia -> la búsqueda podía exponer canales pendientes de
    # revisión aunque no aparecieran en el home.
    channels = (
        ChannelRepository.publishable()
        .filter(name__icontains=q)
        .order_by("name")[:20]
    )

    data = []

    for channel in channels:

        data.append({
            "name": channel.name,
            "slug": channel.slug,
            "country": str(channel.country) if channel.country else "",
            "logo": channel.logo.url if channel.logo else "",
        })

    return JsonResponse(data, safe=False)