from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, HttpResponseNotFound


def city_datasource(request, slug):
    try:
        data_source = CityDataSource.objects.get(slug=slug)
    except CityDataSource.DoesNotExist:
        return HttpResponseNotFound("Doesn't exist")

    context = {
        "data_source": data_source
    }

    return render("city_resource/datasource.html", context=context)
