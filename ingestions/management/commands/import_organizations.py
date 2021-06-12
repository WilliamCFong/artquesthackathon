from django.core.management.base import BaseCommand, CommandError
from people.models import Organization
from .import_base import Command as ImportBase
import pandas as pd
import os

cols = ["Organization", "DepartmentID"]

class Command(ImportBase):
    help = "Import organization data"

    def handle(self, *args, **options):
        path = os.path.expanduser(options["path"])
        df = pd.read_csv(path)

        bucket = {}

        for dep, id_ in df[cols].to_records(index=False):
            bucket[id_] = dep

        for id_, organization in bucket.items():
            organization, created = Organization.objects.get_or_create(pk=id_)
            if created:
                organization.name = dep
                self.stdout.write(
                    f"Creating {organization}"
                )
                organization.save()
            else:
                self.stdout.write(
                    f"Updating {organization}"
                )
