from django.db import models
from people.models import Artist, Organization
from locations.models import Location


class Category(models.Model):
    name = models.CharField(max_length=128, )

    class Meta:
        verbose_name_plural = "categories"


class Status(models.Model):
    name = models.CharField(max_length=128, unique=True)


class Work(models.Model):
    pac = models.IntegerField(primary_key=True)

    # Begin relational models
    categories = models.ManyToManyField(Category)
    artists = models.ManyToManyField(Artist)
    organizations = models.ManyToManyField(Organization)


class Iteration(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    iteration = models.IntegerField()
    iteration_date = models.DateField()


class Piece(models.Model):
    iteration = models.ForeignKey(Iteration, on_delete=models.CASCADE)

    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.RESTRICT)
    zipcode = models.CharField(max_length=128, null=True, blank=True)
    title = models.CharField(max_length=128, null=True, blank=True)
