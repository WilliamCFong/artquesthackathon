from rest_framework.decorators import api_view
from rest_framework.response import Response
from city_resource.models import CityDataSource
from city_resource.serializers import CityDataSourceSerializer


@api_view(["GET"])
def city_datasource(request, slug):
    try:
        resource = CityDataSource.objects.get(slug=slug)
    except CityDataSource.DoesNotExist:
        return Response({"msg": f"Could not find {slug}"}, status=404)

    return Response(
        CityDataSourceSerializer(resource).data,
        status=200
    )
