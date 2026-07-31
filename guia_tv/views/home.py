from django.shortcuts import render

from guia_tv.services.home_service import HomeService


def home(request):

    context = HomeService.get_home_context(

        country=request.GET.get("country"),

        category=request.GET.get("category"),

    )

    return render(
        request,
        "guia_tv/index.html",
        context,
    )