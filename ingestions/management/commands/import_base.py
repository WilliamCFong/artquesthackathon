from django.core.management.base import BaseCommand, CommandError


class ImportURL(BaseCommand):
    help = "Import CABQ data from a url"
    base_url = None

    def add_arguments(self, parser):
        parser.add_argument("--url_override", type=str)
