from django.http import JsonResponse
from guia_tv.models import Channel


def search_channels(request):

    q = request.GET.get("q", "").strip()

    channels = (
        Channel.objects.filter(
            is_active=True,
            name__icontains=q,
        )
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