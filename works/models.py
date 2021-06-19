from polymorphic.models import PolymorphicModel
from djmoney.models.fields import MoneyField
from django.contrib.gis.db import models
from people.models import Individual, Organization
from spacetime.models import TimeSeries, SpaceTimePoint
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

class Location(SpaceTimePoint):
    art = models.ForeignKey(Art, on_delete=models.CASCADE)
    spatial = models.CharField(max_length=256, null=True, blank=True)
    site = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return f"{self.point} on {self.timestamp}"


class EventType(SlugNameMixin):
    def __str__(self):
        return "EventType {self.name}"


class Event(TimeSeries):
    event_type = models.ForeignKey(EventType, on_delete=models.RESTRICT)
    art = models.ForeignKey(Art, on_delete=models.CASCADE)

    contributers = models.ManyToManyField(Individual)


class Valuation(Event):
    amount = MoneyField(max_digits=19, decimal_places=2, default_currency="USD")

    class Meta:
        indexes = [
            BrinIndex(name="money_idx", fields=["amount"]),
        ]
