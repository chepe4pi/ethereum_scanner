from django.core.management.base import BaseCommand, CommandError

from ethereum_scanner.celery import set_web3_filter_task


class Command(BaseCommand):
    help = 'Sync local database with blockchain from current position to end block'

    def add_arguments(self, parser):
        parser.add_argument('async', nargs='?', default='async')

    # TODO logger - synced
    def handle(self, *args, **options):

        async_start = options['async']
        if async_start is 'async':
            set_web3_filter_task.delay()
            self.stdout.write(self.style.SUCCESS('Successfully sync started'))
        else:
            set_web3_filter_task()
            self.stdout.write(self.style.SUCCESS('Successfully synced'))
