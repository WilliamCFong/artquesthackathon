from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from people.models import Organization
from works.models import Work, Iteration
from .import_base import Command as ImportBase
from .utils import get_artist_by_maker, get_pac
import pandas as pd
import os
from math import isnan
from dateutil import parser


class Command(ImportBase):
    help = "Import art"

    def handle(self, *args, **options):
        path = os.path.expanduser(options["path"])
        df = pd.read_csv(path)

        bucket = {}

        for _, row in df.iterrows():
            pac_info = get_pac(row["Object Number"])
            work, created = Work.objects.get_or_create(pac=pac_info["pac"])
            if created:
                work.save()
                print(f"Created {work}")
            else:
                print(f"Updating {work}")

            try:
                artist, created = get_artist_by_maker(row["Maker"])
                if created:
                    artist.save()
                    work.artists.add(artist)
                else:
                    if artist not in work.artists.all():
                        work.artists.add(artist)
            except AttributeError:
                pass

            subpac = pac_info["subpac"]
            iteration, created = Iteration.objects.get_or_create(
                work=work,
                iter_n=subpac,
            )

            if created:
                iteration.name = row["Title"]
                date = row["Stated Date"]
                if date:
                    try:
                        date = parser.parse(date)
                    except TypeError:
                        print(f"\tBad date {date}")
                        date = None
                else:
                    date = None
                iteration.iteration_date = date

                lon = row["Latitude"] # uh oh
                lat = row["Longitude"]
                if all(not isnan(x) for x in [lat, lon]):
                    iteration.location = Point(lat, lon)
                    print(f"\tLoc: {iteration.location}")

                iteration.save()
                print(f"Created {iteration}")
