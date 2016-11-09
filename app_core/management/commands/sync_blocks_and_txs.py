from django.core.management.base import BaseCommand, CommandError

from app_core.connectors import RpcServerConnector
from app_sync.sync_rpc_server import sync_blocks


class Command(BaseCommand):
    help = 'Sync local database with blockchain'

    def add_arguments(self, parser):
        parser.add_argument(
            '--block-start',
            action='store_true',
            dest='block-start',
            default=1844185,
            help='Number of block to start sync',
        )

        parser.add_argument(
            '--block-end',
            action='store_true',
            dest='block-end',
            default=1844286,
            help='Number of block to end sync',
        )

    # TODO logger - synced
    def handle(self, *args, **options):
        web3 = RpcServerConnector().get_connection()
        if not web3.isConnected():
            raise CommandError('Unable to make %s' % web3.currentProvider)
        del web3

        end_block = options['block-end']
        start_block = options['block-start']

        sync_blocks(start_block, end_block)

        self.stdout.write(self.style.SUCCESS('Successfully synced "%s" blocks' % (end_block - start_block + 1)))
