# coding=utf-8
from __future__ import unicode_literals

import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core import validators
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
from size_restricted_image_field import SizeRestrictedImageField
from supported_languages import SupportedLanguages

# USERS
class NextgisUserManager(BaseUserManager):
    """
    Полная копия UserManager
    """
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class NextgisUser(AbstractBaseUser, PermissionsMixin):
    """
    Полная копия стандартного User
    + дополнительные поля:
    nextgis_guid
    """
    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                _('Enter a valid username. This value may contain only '
                  'letters, numbers ' 'and @/./+/-/_ characters.')
            ),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    #  custom fields
    nextgis_guid = models.UUIDField(_('nextgis guid'), default=uuid.uuid4, editable=False, unique=True)
    locale = models.CharField(_('user locale'),
                              max_length=30, null=True, blank=False,
                              choices=SupportedLanguages.dict_text.items(),
                              default=SupportedLanguages.DEFAULT)
    email_confirmed = models.BooleanField(_('mail confirmed'), default=False)

    @property
    def nextgis_id(self):
        return self.id

    objects = NextgisUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


# ICONS
class ServiceIcon(models.Model):

    guid = models.UUIDField(_('icon guid'), default=uuid.uuid4, editable=False)
    icon = SizeRestrictedImageField(_('icon'), upload_to='service_icon/', max_length=200,
                             null=False, blank=False, max_upload_size=2.0)
    name = models.CharField(_('icon name'), max_length=200, null=False, blank=False, unique=True)
    is_private = models.BooleanField(_('icon is private'), default=False)

    def __str__(self):
        return self.name

# SERVICES
@python_2_unicode_compatible
class GeoService(models.Model):
    service_type = 'generic'

    def save(self, *args, **kwargs):
        self.type = self.service_type
        super(GeoService, self).save(*args, **kwargs)

    guid = models.UUIDField(_('service guid'), default=uuid.uuid4, editable=False)
    name = models.CharField(_('service name'), unique=True, max_length=100, blank=False, null=False)
    desc = models.TextField(_('description'), blank=True, null=True)
    type = models.CharField(_('service type'), max_length=20, editable=False, null=False)
    epsg = models.IntegerField(_('EPSG Code'), null=True, blank=True)
    icon = models.ForeignKey(ServiceIcon, models.SET_NULL, blank=True, null=True)
    # license
    license_name = models.CharField(_('license name'), max_length=256, blank=True, null=True)
    license_url = models.URLField(_('license url'), blank=True, null=True)
    copyright_text = models.CharField(_('copyright text'), max_length=2048, blank=True, null=True)
    copyright_url = models.URLField(_('copyright url'), blank=True, null=True)
    terms_of_use_url = models.URLField(_('terms of use url'), blank=True, null=True)
    # creation & update info
    submitter = models.ForeignKey(NextgisUser, on_delete=models.SET_NULL, to_field='nextgis_guid', null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    # source info
    source = models.CharField(_('source'), max_length=2048, blank=True, null=True)
    source_url = models.URLField(_('source url'), blank=True, null=True)

    # tags


    def __str__(self):
        return self.name


class TmsService(GeoService):
    service_type = 'tms'

    url = models.URLField(blank=False, null=False)
    z_min = models.IntegerField(blank=True, null=True)
    z_max = models.IntegerField(blank=True, null=True)
    y_origin_top = models.BooleanField(default=False, blank=True)


class WmsService(GeoService):
    OUTPUT_FORMATS = (
        ('image/png', 'PNG'),
        ('image/png8', 'PNG8'),
        ('image/png24', 'PNG24'),
        ('image/png32', 'PNG32'),
        ('image/gif', 'GIF'),
        ('image/bmp', 'BMP'),
        ('image/jpeg', 'JPEG'),
        ('image/tiff', 'TIFF'),
        ('image/tiff8', 'TIFF8'),
        ('image/geotiff', 'GeoTIFF'),
        ('image/geotiff8', 'GeoTIFF8'),
        ('image/svg+xml', 'SVG')
    )

    service_type = 'wms'

    url = models.URLField(blank=False, null=False)
    params = models.CharField(max_length=1024, blank=True, null=True)
    layers = models.CharField(max_length=1024, blank=True, null=True)
    turn_over = models.BooleanField(default=False, blank=True)
    format = models.CharField(max_length=128, blank=True, null=True, choices=OUTPUT_FORMATS)


class WfsService(GeoService):
    service_type = 'wfs'

    url = models.URLField(blank=False, null=False)
    layer = models.CharField(_('Layer name ([namespace:]featuretype)'), max_length=1024, blank=False, null=False)


class GeoJsonService(GeoService):
    service_type = 'geojson'

    url = models.URLField(blank=False, null=False)
