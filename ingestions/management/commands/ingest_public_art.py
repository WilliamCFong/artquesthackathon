from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from .import_base import ImportUrl
from .utils import get_artist_by_maker, get_pac
from city_resource.models import CityDataSource
import pandas as pd


CABQ_PUBLIC_DATANAME = "Public Art"


class Command(ImportUrl):
    help = "Import ABQ Public Art data"
    base_url = "http://data.cabq.gov/community/art/publicartv2/CABQPublicArt.csv"


    def handle(self, *args, **kwargs):
        url = kwargs.pop("url_override", base_url)
        # Assume csv
        df = pd.read_csv(url)

        with transaction.atomic()
            public_art, created = CityDataSource.objects.get_or_create(name=CABQ_PUBLIC_DATANAME)
            if created:
                self.stdout.write(
                    f"Adding {public_art}"
                )
                public_art.save()

            for idx, row in df.iterrows():
                pac_info = get_pac(row["Object Number"])
                art, created = Art.objects.get_or_create(pac=pac_info["pac"], data_source=public_art)
                if created:
                    f"Creating {art}"
                    art.title = row["Title"]
                    art.save()


