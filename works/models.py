from django.contrib.gis.db import models
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

    def __str__(self):
        return f"PAC {self.pac}"

    def get_absolute_url(self):
        return f"/works/{self.pac}/"

    def most_recent_loc(self):
        iteration = (
            self
            .iterations
            .filter(location__isnull=False)
            .order_by("-iteration_date")
            .first()
        )
        return iteration.location


class Iteration(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="iterations")
    iter_n = models.IntegerField()
    iteration_date = models.DateField(null=True)
    location = models.PointField(null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    zipcode = models.CharField(max_length=128, null=True, blank=True)
    title = models.CharField(max_length=128, null=True, blank=True)


    def __str__(self):
        return f"{self.title}"
