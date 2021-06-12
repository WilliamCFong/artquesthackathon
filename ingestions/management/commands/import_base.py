from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Import ABQ Public Data csv"

    def add_arguments(self, parser):
        parser.add_argument("path", type=str)
