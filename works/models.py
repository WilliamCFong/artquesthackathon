from polymorphic.models import PolymorphicModel
from djmoney.models.fields import MoneyField
from django.contrib.gis.db import models
from people.models import Individual, Organization
from spacetime.models import TimeSeries
from django.contrib.postgres.indexes import BrinIndex
from city_resource.models import CityData


class Category(models.Model):
    name = models.CharField(max_length=128, )

    class Meta:
        verbose_name_plural = "categories"


class Art(CityData):
    pac = models.IntegerField(unique=True)
    title = models.CharField(max_length=128)

    # Begin relational models
    artists = models.ManyToManyField(Individual)
    categories = models.ManyToManyField(Category)
    organizations = models.ManyToManyField(Organization)

    def __str__(self):
        return f"PAC {self.pac}"

    def get_absolute_url(self):
        return f"/works/{self.pac}/"


class Event(TimeSeries):
    art = models.ForeignKey(Art)


class Valuation(Event):
    valuation_type = models.CharField(max_length=128)
    amount = MoneyField(default_currency="USD")

    class Meta:
        indexes = [
            BrinIndex(name="money_idx", fields=["amount"]),
        ]


class Work(Event):
    work_type = models.CharField(max_length=128)
    contributers = models.ManyToManyField(Individual)
