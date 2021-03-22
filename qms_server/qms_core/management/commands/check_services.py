import datetime
import multiprocessing
import pprint
import time

from django.core.management import BaseCommand

from qms_core.models import (
    GeoService,
    TmsService,
    WmsService,
    WfsService,
    GeoJsonService,
)
from qms_core.status_checker.status_checker import check_by_id, check_by_id_and_save


class Command(BaseCommand):
    help = 'Check services in db'
    output_transaction = True

    def add_arguments(self, parser):
        service_type_choices = [TmsService.service_type, WmsService.service_type, WfsService.service_type, GeoJsonService.service_type]

        parser.add_argument('-t', '--threads', help='Threads count for checkers', type=int, default=20)
        parser.add_argument('--service_type', choices=service_type_choices, help='Service type')
        parser.add_argument('--service', help='Internal service id', type=int)
        
        parser.add_argument('--sleep_afte_check_until_endofday', action='store_true', help='Wait end of day after check')



    def handle(self, *args, **options):
        thread_count = options['threads']

        service_ids = GeoService.objects.all().only('id').values_list(flat=True)
        
        if options.get('service'):
            service_ids = service_ids.filter(id=options['service'])
        
        if options.get('service_type'):
            service_ids = service_ids.filter(type=options['service_type'])

        print('Try to check %s services' % len(service_ids))

        start_day = datetime.date.today()

        checkers_pool = multiprocessing.Pool(thread_count)
        checkers_pool.imap(check_by_id_and_save, service_ids)
        checkers_pool.close()
        checkers_pool.join()


        if options.get('sleep_afte_check_until_endofday'):
            print('Wait end of day ...')
            while start_day == datetime.date.today():
                time.sleep(60 * 5)
            print('Bye!')
