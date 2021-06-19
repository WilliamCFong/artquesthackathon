from django.core.management.base import BaseCommand, CommandError
from djmoney.money import Money
from django.db import transaction
from .import_base import ImportUrl
from .utils import get_individual_by_maker, get_pac, normalize_event_type
from works.models import EventType, Event, Valuation, Art
from dateutil import parser
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

        with transaction.atomic():
            public_art, created = CityDataSource.objects.get_or_create(name=CABQ_PUBLIC_DATANAME)
            if created:
                self.stdout.write(
                    f"Adding {public_art}"
                )
                public_art.save()

            for idx, row in df.iterrows():
                art = self.handle_art(public_art, row)
                if row["Event Type"] and row["Historical Date"]:
                    event = self.handle_event_type(art, row)
                    contributer = self.handle_contributer(event, row)

                if row["ValuationPurpose"]:
                    valuation = self.handle_valuation(art, row)

                if row["Longitude"] and row["Latitude"]:
                    location = self.handle_location(art, row)

                if row["ValuationPurpose"]:
                    self.handle_valuation(art, row)

    def handle_art(self, data_source, row):
        pac_info = get_pac(row["Object Number"])
        art, created = (
            Art
            .objects
            .get_or_create(
                pac=pac_info["pac"],
                data_source=data_source
            )
        )
        if created:
            f"Adding {art}"
            art.title = row["Title"]
            art.description = row["Description"]
            art.save()

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

        timestamp = parser.parse(row["Historical Date"])

        event_type, created = EventType.objects.get_or_create(name=name)
        if created:
            self.stdout.write(f"Adding {event_type}")
            event_type.save()

        event, created = (
            EventType
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
        timestamp = parser.parse(row["Stated Date"])
        usd = Money(row["Stated Value"], "USD")

        event_type, created = EventType.objects.get_or_create(name=name)

        if created:
            self.stdout.write(f"Adding {event_type}")
            event_type.save()

        valuation, created = (
            Valuation
            .objects
            .get_or_create(
                art=current_art,
                event_type=event_type,
                timestamp=timestamp,
            )
        )

        if created:
            valuation.amount = usd
            self.stdout.write(f"Adding {valuation}")
            valuation.save()
        elif valuation.amount != usd:
            self.stdout.write(f"Updating {valuation} to {usd}")
            valuation.amount = usd
            valuation.save()

        return valuation

    def handle_location(self, current_art, row):
        timestamp = parser.parse(row["Stated Date"])
        location, created = (
            Location
            .objects
            .get_or_create(
                art=current_art,
                timestamp=timestamp
            )
        )
        if self.LEGACY:
            location.latitude = row["Longitude"]
            location.longitude = row["Latitude"]
        else:
            location.latitude = row["Latitude"]
            location.longitude = row["Longitude"]

        if created:
            self.stdout.write(f"Added {location}")
            location.save()
        else:
            self.stdout.write(f"Updated {location}")
