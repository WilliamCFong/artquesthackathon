from polymorphic.models import PolymorphicModel
from django.db import models
from django.utils.text import slugify
from artquest.mixins import SlugNameMixin


class CityDataSource(SlugNameMixin):
    city_url = models.URLField()


class CityData(PolymorphicModel):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)
    data_source = models.ForeignKey(CityDataSource, on_delete=models.RESTRICT)

    class Meta:
        pass

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
