from django.core.management.base import BaseCommand, CommandError
from djmoney.money import Money
from django.db import transaction
from django.contrib.gis.geos import Point
from .import_base import ImportURL
from .utils import get_individual_by_maker, get_pac, normalize_event_type, get_timestamp
from works.models import EventType, Event, Valuation, Art, Location
from city_resource.models import CityDataSource
from math import isnan
import pandas as pd


CABQ_PUBLIC_DATANAME = "Public Art"


class Command(ImportURL):
    help = "Import ABQ Public Art data"
    base_url = "http://data.cabq.gov/community/art/publicartv2/CABQPublicArt.csv"
    LEGACY = True

    def handle(self, *args, **kwargs):
        url = self.base_url
        if kwargs.get("url_override", ""):
            url = kwargs.pop("url_override")
        # Assume csv
        self.stdout.write(f"Requesting data at {url}")
        df = pd.read_csv(url, encoding="ISO-8859-1")

        with transaction.atomic():
            public_art, created = CityDataSource.objects.get_or_create(name=CABQ_PUBLIC_DATANAME)
            public_art.city_url = url
            if created:
                self.stdout.write(
                    f"Adding {public_art}"
                )
            public_art.save()

            for idx, row in df.iterrows():
                art = self.handle_art(public_art, row)

                if row["Event Type"] and row["Historical Date"]:
                    event = self.handle_event_type(art, row)
                    if event is None:
                        continue

                    if isinstance(row["Maker"], str):
                        contributer = self.handle_contributer(event, row)
                        event.contributers.add(contributer)

                if isinstance(row["ValuationPurpose"], str):
                    valuation = self.handle_valuation(art, row)

                check = any(isnan(row[col]) for col in ["Longitude", "Latitude"])
                if not check:
                    location = self.handle_location(art, row)


    def handle_art(self, data_source, row):
        pac_info = get_pac(row["Object Number"])
        try:
            art = (
                Art
                .objects
                .get(
                    pac=pac_info["pac"],
                    data_source=data_source
                )
            )
        except Art.DoesNotExist:
            art = Art(
                pac=pac_info["pac"],
                data_source=data_source,
                title=row["Title"],
                description=row["Description"]
            )
            f"Adding {art}"
            art.save()

        return art

    def handle_category(self, current_art, row):
        name = row["Classification"]
        category, created = (
            Category
            .objects
            .get_or_create(
                name=name
            )
        )
        if created:
            category.save()

    def handle_event_type(self, current_art, row):
        name = normalize_event_type(row["Event Type"])
        try:
            timestamp = get_timestamp(row["Historical Date"])
        except:
            self.stderr.write(
                f"Row {row} does not have a proper historical date"
            )
            return None

        event_type, created = EventType.objects.get_or_create(name=name)
        if created:
            self.stdout.write(f"Adding {event_type}")
            event_type.save()

        event, created = (
            Event
            .objects
            .get_or_create(
                event_type=event_type,
                art=current_art,
                timestamp=timestamp
            )
        )

        if created:
            self.stdout.write(
                f"Adding {event}"
            )
            event.save()
        return event

    def handle_contributer(self, current_event, row):
        individual, created = get_individual_by_maker(row["Maker"])
        if created:
            self.stdout.write(
                f"Adding {individual}"
            )
            individual.save()
        if individual not in current_event.contributers.all():
            self.stdout.write(
                f"Adding {individual} to {current_event} contributers"
            )
            current_event.contributers.add(individual)
        return individual

    def handle_valuation(self, current_art, row):
        name = normalize_event_type(row["ValuationPurpose"])
        timestamp = get_timestamp(row["Stated Date"])
        usd = Money(row["Stated Value"], "USD")

        event_type, created = EventType.objects.get_or_create(name=name)

        if created:
            self.stdout.write(f"Adding {event_type}")
            event_type.save()

        try:
            valuation = (
                Valuation
                .objects
                .get(
                    art=current_art,
                    event_type=event_type,
                    timestamp=timestamp,
                )
            )
            if valuation.amount != usd:
                self.stdout.write(f"Updating {valuation} to {usd}")
                valuation.amount = usd

        except Valuation.DoesNotExist:
            valuation = (
                Valuation(
                    art=current_art,
                    event_type=event_type,
                    timestamp=timestamp,
                    amount=usd
                )
            )
            self.stdout.write(f"Adding {valuation}")
        valuation.save()
        
        return valuation

    def handle_location(self, current_art, row):
        timestamp = get_timestamp(row["Historical Date"])
        if self.LEGACY:
            latitude = row["Longitude"]
            longitude = row["Latitude"]
        else:
            latitude = row["Latitude"]
            longitude = row["Longitude"]
        pos = Point(latitude, longitude)

        try:
            location = (
                Location
                .objects
                .get(
                    art=current_art,
                    timestamp=timestamp
                )
            )
            self.stdout.write(f"Updated {location}")
        except Location.DoesNotExist:
            location = Location(
                art=current_art,
                timestamp=timestamp,
                point=pos
            )
            self.stdout.write(f"Added {location}")
        location.save()
