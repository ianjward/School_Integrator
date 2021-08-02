from django.core.management.base import BaseCommand, CommandError
from ...models import update_chromebooks


class Command(BaseCommand):
    help = 'Pulls the latest Chromebook statuses from Google'

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         '--delete',
    #         action='store_true',
    #         help='Delete poll instead of closing it',
    #     )

    def handle(self, *args, **options):
        update_chromebooks()
