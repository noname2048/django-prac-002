from django.core.management.base import BaseCommand, CommandError
from instagram.models import Post


class Command(BaseCommand):
    help = "make Post!"

    def add_arguments(self, parser):
        parser.add_argument("poll_ids", nargs="+, type=int")