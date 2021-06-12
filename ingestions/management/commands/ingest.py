from django.core.management.base import BaseCommand, CommandError
from .import_base import Command as ImportBase
import pandas as pd
import numpy as np
import os


class Command(ImportBase):
    help = "Import ABQ Public Data csv"

    def handle(self, *args, **options):
        path = os.path.expanduser(options["path"])
        df = pd.read_csv(path)

        # ABQ SWAPS LON AND LAT!
        actual_lat = np.array(df["Longitude"])
        actual_lon = np.array(df["Latitude"])

        df["Longitude"] = actual_lon
        df["Latitude"] = actual_lat
