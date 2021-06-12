from django.contrib.gis.db import models

# Create your models here.
class Location(models.Model):
    location = models.PointField()
