import multiprocessing
import pprint

from django.core.management import BaseCommand
from django.db.models import F

from qms_core.models import GeoService
from qms_core.status_checker.status_checker import check_by_id, check_by_id_and_save


class Command(BaseCommand):
    help = 'Set updated_at to created_at'
    output_transaction = True

    def handle(self, *args, **options):
        print('WARNING! This command update all records of geoservices! Type "yes" to continue')
        input = raw_input()
        if input == 'yes':
            for geoservice in GeoService.objects.all():
                geoservice = geoservice.get_typed_instance()
                geoservice.boundary_area = geoservice.boundary.area if geoservice.boundary else None
                geoservice.save()
        else:
            print('incorrect input')
