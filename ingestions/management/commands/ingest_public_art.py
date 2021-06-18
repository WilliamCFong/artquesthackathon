from django.core.management.base import BaseCommand, CommandError
from .import_base import ImportUrl
from city_resource.models import CityDataSource
import pandas as pd


CABQ_PUBLIC_DATANAME = "Public Art"


class Command(ImportUrl):
    help = "Import ABQ Public Art data"
    base_url = "http://data.cabq.gov/community/art/publicartv2/CABQPublicArt.csv"


    def get_artists(self, df):
        new_artists = {}
        artists = df["Maker"]

    def get_art(self, df):
        pass

    def get_events(self, df):
        pass

    def get_locations(self, df):
        pass

    def handle(self, *args, **kwargs):
        url = kwargs.pop("url_override", base_url)
        models_to_add = []  # Must be saved in-order to satisfy fk constraints
        # Assume csv
        df = pd.read_csv(url)

        public_art, created = CityDataSource.objects.get_or_create(name=CABQ_PUBLIC_DATANAME)
        if created:
            self.stdout.write(
                f"Enqueing {public_art} for creation"
            )
            models_to_add.append(public_art)

        # Grab Artists
        raise NotImplementedError

        # Define Works
        raise NotImplementedError
