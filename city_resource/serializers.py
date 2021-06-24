from rest_framework import serializers
from city_resource.models import CityDataSource


class CityDataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityDataSource
        fields = ["city_url", "name", "slug"]
