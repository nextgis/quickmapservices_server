from django.core.exceptions import ValidationError
from django.db.models import ImageField
from django.utils.translation import ugettext as _


class SizeRestrictedImageField(ImageField):
    def __init__(self, verbose_name=None, name=None, width_field=None,
                 height_field=None, max_upload_size=1.0, **kwargs):
        self.max_upload_size = max_upload_size
        super(SizeRestrictedImageField, self).__init__(verbose_name, name, width_field, height_field, **kwargs)

    def clean(self, data, initial=None):
        file_obj = super(SizeRestrictedImageField, self).clean(data, initial)

        if file_obj.size > self.max_upload_size * 1024 * 1024:
            raise ValidationError(_('Max file size is %s MB') % str(self.max_upload_size))

        return data
