from polymorphic.models import PolymorphicModel
from django.contrib.gis.db import models
from django.contrib.postgres.indexes import BrinIndex, GistIndex


class TimeSeries(PolymorphicModel):
    timestamp = models.DateTime(null=False)

    class Meta:
        indexes = [
            BrinIndex(name="timestamp_idx", fields=["timestamp"]),
        ]
        ordering = "-timestamp"  # by default, order from most recent

class SpatialPoint(PolymorphicModel):
    point = models.PointField()

    class Meta:
        indexes = [
            GistIndex(name="point_space_idx", fields=["point"]),
        ]

class SpatialPolygon(PolymorphicModel):
    geometry = models.MultiPolygonField()

    class Meta:
        indexes = [
            GistIndex(name="geometry_space_idx", fields=["geometry"]),
        ]
