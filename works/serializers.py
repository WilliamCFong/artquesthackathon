from rest_framework import serializers
from works.models import Art, Location


class ArtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Art
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["timestamp", "point"]
        geo_field = "point"

class LocationPACSerializer(serializers.ModelSerializer):
    art = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Location
        fields = ["art", "timestamp", "point"]
        geo_field = "point"
