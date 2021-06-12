from django.db import models


class Artist(models.Model):
    first_name = models.CharField(max_length=128, )
    middle_name = models.CharField(max_length=128, )
    last_name = models.CharField(max_length=128, )

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"<Artist {self.fullname}>"


class Organization(models.Model):
    name = models.CharField(max_length=128, )


    def __str__(self):
        return f"{self.name}.org"
