import multiprocessing
import pprint

from django.core.management import BaseCommand

from qms_core.models import GeoService
from qms_core.status_checker.status_checker import check_by_id, check_by_id_and_save


class Command(BaseCommand):
    help = 'Check services in db'
    output_transaction = True

    def add_arguments(self, parser):
        parser.add_argument('-t', '--threads', help='Threads count for checkers', type=int, default=20)
        parser.add_argument('--service', help='Internal service id', type=int)



    def handle(self, *args, **options):
        thread_count = options['threads']

        if options.get('service'):
            service_ids = [options['service']]
        else:
            service_ids = GeoService.objects.all().only('id').values_list(flat=True)

        checkers_pool = multiprocessing.Pool(thread_count)
        checkers_pool.imap(check_by_id_and_save, service_ids)
        checkers_pool.close()
        checkers_pool.join()

