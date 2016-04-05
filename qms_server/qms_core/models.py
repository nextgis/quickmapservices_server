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

# Create your models here.
from supported_languages import SupportedLanguages


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
    nextgis_guid = models.UUIDField(_('nextgis guid'), default=uuid.uuid4, editable=False)
    locale = models.CharField(_('user locale'),
                              max_length=30, null=True, blank=False,
                              choices=SupportedLanguages.dict_text.items(),
                              default=SupportedLanguages.DEFAULT)

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

    #license
    #tags
    #icon


class TmsService(GeoService):
    service_type = 'tms'

    url = models.URLField(blank=False, null=False)
    z_min = models.IntegerField(blank=True, null=True)
    z_max = models.IntegerField(blank=True, null=True)
    y_origin_top = models.BooleanField(default=False, blank=True)


class WmsService(GeoService):
    service_type = 'wms'

    url = models.URLField(blank=False, null=False)
    params = models.CharField(max_length=1024, blank=True, null=True)
    layers = models.CharField(max_length=1024, blank=True, null=True)
    turn_over = models.BooleanField(default=False, blank=True)


class WfsService(GeoService):
    service_type = 'wfs'

    url = models.URLField(blank=False, null=False)


#self.gdal_source_file = None
