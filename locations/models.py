from django.contrib.gis.db import models
from spacetime.models import TimeSeries, SpatialPoint, SpatialPolygon

class Location(TimeSeries, SpatialPoint):
    zipcode= models.CharField(max_length=10, blank=True, null=True)
    pass
