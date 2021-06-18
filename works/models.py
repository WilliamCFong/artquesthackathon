from polymorphic.models import PolymorphicModel
from djmoney.models.fields import MoneyField
from django.contrib.gis.db import models
from people.models import Individual, Organization
from spacetime.models import TimeSeries, SpatialPoint
from artquest.mixins import SlugNameMixin
from django.contrib.postgres.indexes import BrinIndex
from city_resource.models import CityData


class Category(SlugNameMixin):
    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return f"{self.name}"


class Art(CityData):
    pac = models.IntegerField(unique=True)
    title = models.CharField(max_length=128)

    description = models.TextField(null=True)

    # Begin relational models
    categories = models.ManyToManyField(Category)
    organizations = models.ManyToManyField(Organization)

    def __str__(self):
        return f"PAC {self.pac}"

    def get_absolute_url(self):
        return f"/works/{self.pac}/"

class Location(TimeSeries, SpatialPoint):
    art = models.ForeignKey(Art)
    location = models.CharField(length=256, null=True, blank=True)
    site = models.CharField(length=256, null=True, blank=True)

    def __str__(self):
        return f"{self.point} on {self.timestamp}"


class EventType(SlugNameMixin):
    def __str__(self):
        return "EventType {self.name}"

class Event(TimeSeries):
    event_type = models.ForeignKey(EventType)
    art = models.ForeignKey(Art)

    contributers = models.ManyToManyField(Individual)


class Valuation(Event):
    amount = MoneyField(default_currency="USD")

    class Meta:
        indexes = [
            BrinIndex(name="money_idx", fields=["amount"]),
        ]
