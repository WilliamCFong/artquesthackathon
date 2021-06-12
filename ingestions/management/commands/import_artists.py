from django.core.management.base import BaseCommand, CommandError
from .import_base import Command as ImportBase
from .utils import get_artist_by_maker
import pandas as pd
import numpy as np
import os


class Command(ImportBase):
    help = "Import artist data"

    def handle(self, *args, **options):
        path = os.path.expanduser(options["path"])
        df = pd.read_csv(path)

        bucket = {}

        for maker_name, group in df.groupby("Maker"):
            artist, created = get_artist_by_maker(maker_name)
            if created:
                self.stdout.write(
                    f"Creating {artist}"
                )
                artist.save()
            else:
                self.stdout.write(
                    f"Updating {artist}"
                )
