import datetime
import logging
import multiprocessing
import time
from django.conf import settings
from django import db

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
        logger = logging.getLogger('qms_checking')
        while True:
            today = datetime.datetime.today()
            curr_hour = today.hour
            hour = settings.CHECKING_SERVICES_HOUR_UTC
            if curr_hour == hour:
                self._do_handle(options, logger)
                seconds_sleep = 3600 + 1
                logger.info(f'sleeping {seconds_sleep} seconds after checking services')
                time.sleep(seconds_sleep)
            else:
                seconds_sleep = 60 * 30
                logger.info(f'bad time for checking services (waiting for hour {hour} UTC, now is hour {curr_hour} UTC), sleeping {seconds_sleep} seconds')
                time.sleep(seconds_sleep)

    def _do_handle(self, options, logger):
        thread_count = options['threads']

        service_ids = GeoService.objects.all().only('id').values_list(flat=True)
        
        if options.get('service'):
            service_ids = service_ids.filter(id=options['service'])
        
        if options.get('service_type'):
            service_ids = service_ids.filter(type=options['service_type'])

        services_count = len(service_ids)
        logger.info(f'trying to check {services_count} services in {thread_count} threads')

        db.connections.close_all()

        checkers_pool = multiprocessing.Pool(thread_count)
        with checkers_pool as pool:
            imap_result = pool.imap(check_by_id_and_save, service_ids)
            for i, _ in enumerate(imap_result):
                logger.info('\rchecking progress: {0:%}'.format(i / services_count))
            pool.close()
            pool.join()
            logger.info('checking finished')
