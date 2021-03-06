from __future__ import print_function
import json
import tempfile
import urllib2
from zipfile import ZipFile

import os
import shutil

from django.core.files import File
from django.core.management import BaseCommand

from .qms_plugin.data_source_serializer import DataSourceSerializer
from .qms_plugin.supported_drivers import KNOWN_DRIVERS
from qms_core.models import GeoService, TmsService, WmsService, WfsService, ServiceIcon

__author__ = 'yellow'


class Command(BaseCommand):
    help = 'Import existing services from github'
    output_transaction = True

    REPOS_INFO = {
        'contrib': {
            'url': 'https://api.github.com/repos/nextgis/quickmapservices_contrib',
            'subdir': 'data_sources',
        },
        'base': {
            'url': 'https://api.github.com/repos/nextgis/quickmapservices',
            'subdir': 'src/data_sources',
        }
    }

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Remove existing data and create new')
        parser.add_argument('--base', action='store_true', help='Import data sources from base repo')
        parser.add_argument('--contrib', action='store_true', help='Import data sources from contrib repo')


    def handle(self, *args, **options):
        if options['clear']:
            GeoService.objects.all().delete()
            ServiceIcon.objects.all().delete()
        if options['base']:
            self.import_from_repo(self.REPOS_INFO['base'])
        if options['contrib']:
            self.import_from_repo(self.REPOS_INFO['contrib'])


    def import_from_repo(self, repo_info):
        count = 0
        services_dir = self.load_contrib_pack(repo_info['url'])
        services_dirs = os.listdir(os.path.join(services_dir, repo_info['subdir']))

        for s_dir in services_dirs:
            src_dir = os.path.join(services_dir, repo_info['subdir'], s_dir)
            metadata_pth = os.path.join(src_dir, 'metadata.ini')
            ds = DataSourceSerializer.read_from_ini(metadata_pth)
            print(ds.alias)

            if ds.type == KNOWN_DRIVERS.TMS:
                service = TmsService(name=ds.alias,
                                     url=ds.tms_url,
                                     z_min=ds.tms_zmin,
                                     z_max=ds.tms_zmax,
                                     epsg=3857)
                if ds.tms_y_origin_top is not None:
                    service.y_origin_top = ds.tms_y_origin_top
                if ds.tms_epsg_crs_id is not None:
                    service.epsg = ds.tms_epsg_crs_id
                self.apply_img(ds, service)
                self.apply_lic(ds, service)
                service.save()

            if ds.type == KNOWN_DRIVERS.WMS:
                service = WmsService(name=ds.alias,
                                     url=ds.wms_url,
                                     params=ds.wms_params,
                                     layers=ds.wms_layers)
                if ds.wms_turn_over is not None:
                    service.turn_over = ds.wms_turn_over
                self.apply_img(ds, service)
                self.apply_lic(ds, service)
                service.save()

            if ds.type == KNOWN_DRIVERS.WFS:
                service = WfsService(name=ds.alias,
                                     url=ds.wfs_url)
                self.apply_img(ds, service)
                self.apply_lic(ds, service)
                service.save()

            if ds.type == KNOWN_DRIVERS.GDAL:
                print('Unsupported service type: %s %s' % (ds.type, ds.alias))
                count -= 1

            count += 1

        self.clean()
        self.stdout.write('Successfully import %s services of %s' % (count, len(services_dirs)))


    def load_contrib_pack(self, url):
        # get info
        latest_release_info = self._get_latest_release_info(url)
        name = latest_release_info['name']
        zip_url = latest_release_info['zipball_url']

        # create temp dir
        self.tmp_dir = tempfile.mkdtemp()

        # download zip file
        zip_file_path = os.path.join(self.tmp_dir, 'repo.zip')
        self._download_file(zip_url, zip_file_path)

        # extract zip to tmp dir
        tmp_extract_dir = os.path.join(self.tmp_dir, 'repo')
        self._extract_zip(zip_file_path, tmp_extract_dir)

        # first dir - our content
        src_dir_name = os.listdir(tmp_extract_dir)[0]
        src_dir = os.path.join(tmp_extract_dir, src_dir_name)

        return src_dir


    def clean(self):
        if self.tmp_dir and os.path.exists(self.tmp_dir):
            # remove tmp dir
            shutil.rmtree(self.tmp_dir, ignore_errors=True)


    def _get_latest_release_info(self, url):
        response = urllib2.urlopen('%s/%s/%s' % (url, 'releases', 'latest'))
        latest_release_info = json.loads(response.read().decode('utf-8'))
        return latest_release_info


    def _download_file(self, url, out_path):
        d_file = urllib2.urlopen(url)
        with open(out_path, 'wb') as output:
            output.write(d_file.read())


    def _extract_zip(self, zip_path, out_path):
        zf = ZipFile(zip_path)
        zf.extractall(out_path)

    def get_exists_img(self, icon_name):
        icons = ServiceIcon.objects.filter(name=icon_name)
        if icons:
            return icons[0]
        else:
            return None

    def apply_img(self, ds, service):
        if ds.icon_path \
                and os.path.exists(ds.icon_path) \
                and os.path.splitext(ds.icon_path)[1] in ('.png', '.jpg'):

            icon_name = os.path.basename(os.path.splitext(ds.icon_path)[0])

            exists_img = self.get_exists_img(icon_name)

            if exists_img:
                service.icon = exists_img
            else:
                new_icon = ServiceIcon(name=icon_name)
                new_icon.icon.save(
                    os.path.basename(ds.icon_path),
                    File(open(ds.icon_path))
                )
                service.icon = new_icon

    def apply_lic(self, ds, service):
        if ds.lic_name:
            service.license_name = ds.lic_name
        if ds.lic_link:
            service.license_url = ds.lic_link
        if ds.copyright_text:
            service.copyright_text = ds.copyright_text
        if ds.copyright_link:
            service.copyright_url = ds.copyright_link
        if ds.terms_of_use:
            service.terms_of_use_url = ds.terms_of_use
