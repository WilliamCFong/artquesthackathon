from django.urls import path, register_converter
from works.models import Art, Location
from rest_framework.response import Response
from works.serializers import ArtSerializer, LocationSerializer, LocationPACSerializer
from rest_framework.decorators import api_view

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance

@api_view(["GET"])
def art(request, pac):
    try:
        art = Art.objects.get(pac=pac)
    except Art.DoesNotExist:
        return Response({"msg": "PAC {pac} does not exist"}, status=404)

    return Response(
        ArtSerializer(art).data,
        status=404
    )

@api_view(["GET"])
def locations(request, pac):
    try:
        art = Art.objects.get(pac=pac)
    except Art.DoesNotExist:
        return Response({"msg": "PAC {pac} does not exist"}, status=404)

    locations = art.locations
    return Response(
        LocationSerializer(locations, many=True).data,
        status=200
    )

@api_view(["GET"])
def most_recent_locations(request):
    locations = (
        Location
        .objects
        .prefetch_related("art")
    )
    return Response(
        LocationPACSerializer(locations.all(), many=True).data,
        status=200
    )


@api_view(["GET"])
def nearby(request):
    try:
        lat = float(request.query_params["lat"])
        lon = float(request.query_params["lon"])
        distance = Distance(
            km=float(request.query_params.get("radius", 10))
        )
    except (TypeError, ValueError):
        return Response({"msg": "Bad parameter"}, status=400)
    except KeyError:
        return Respones({"msg": "Missing parameter"}, status=400)

    point = Point(lat, lon)
    q = (
        Location
        .objects
        .filter(
            point__distance_lt=(point, distance)
        )
    )

    return Response(
        LocationPACSerializer(q.all(), many=True).data,
        status=200
    )


urlpatterns = [
    path("art/<int:pac>/", art, name="art"),
    path("art/<int:pac>/locations/", locations, name="art-locations"),
    path("art/locations/", most_recent_locations, name="all-locations"),
    path("art/nearby/", nearby, name="nearby"),
]
