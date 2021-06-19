from polymorphic.models import PolymorphicModel
from django.db import models
from django.contrib.gis.db.models import PointField, MultiPolygonField
from django.contrib.postgres.indexes import BrinIndex, GistIndex


class TimeSeries(PolymorphicModel):
    timestamp = models.DateTimeField(null=False)

    class Meta:
        indexes = [
            BrinIndex(name="timestamp_idx", fields=["timestamp"]),
        ]
        ordering = ["-timestamp"]  # by default, order from most recent

class SpatialPoint(PolymorphicModel):
    point = PointField()

    class Meta:
        indexes = [
            GistIndex(name="point_space_idx", fields=["point"]),
        ]

class SpatialPolygon(PolymorphicModel):
    geometry = MultiPolygonField()

    class Meta:
        indexes = [
            GistIndex(name="geometry_space_idx", fields=["geometry"]),
        ]

class SpaceTimePoint(PolymorphicModel):
    timestamp = models.DateTimeField(null=False)
    point = PointField()

    class Meta:
        indexes = [
            GistIndex(name="spacetime_point_idx", fields=["point"]),
            BrinIndex(name="spacetimestamp_idx", fields=["timestamp"]),
        ]
        ordering = ["-timestamp"]  # by default, order from most recent


