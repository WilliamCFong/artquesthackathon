from polymorphic.models import PolymorphicModel
from django.db import models
from django.utils.text import slugify
from artquest.mixins import SlugNameMixin


class CityDataSource(SlugNameMixin):
    city_url = models.URLField()


class CityData(PolymorphicModel):
    data_source = models.ForeignKey(CityDataSource, on_delete=models.RESTRICT)
    class Meta:
        pass
