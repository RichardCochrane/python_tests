import os

from django import forms
from django.utils import six
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat

from avatar.conf import settings
from avatar.models import Avatar


def avatar_img(avatar, size):
    if not avatar.thumbnail_exists(size):
        avatar.create_thumbnail(size)
    return mark_safe('<img src="%s" alt="%s" width="%s" height="%s" />' %
                     (avatar.avatar_url(size), six.text_type(avatar),
                      size, size))


class UploadAvatarForm(forms.Form):

    avatar = forms.ImageField(label=_("Avatar"))

    def clean_avatar(self):
        data = self.cleaned_data['avatar']

        if settings.AVATAR_ALLOWED_FILE_EXTS:
            root, ext = os.path.splitext(data.name.lower())
            if ext not in settings.AVATAR_ALLOWED_FILE_EXTS:
                valid_exts = ", ".join(settings.AVATAR_ALLOWED_FILE_EXTS)
                error = _("%(ext)s is an invalid file extension. "
                          "Authorized extensions are : %(valid_exts_list)s")
                raise forms.ValidationError(error %
                                            {'ext': ext,
                                             'valid_exts_list': valid_exts})

        if data.size > settings.AVATAR_MAX_SIZE:
            error = _("Your file is too big (%(size)s), "
                      "the maximum allowed size is %(max_valid_size)s")
            raise forms.ValidationError(error % {
                'size': filesizeformat(data.size),
                'max_valid_size': filesizeformat(settings.AVATAR_MAX_SIZE)
            })

        return data

    def save(self, contact):
        Avatar(contact=contact, avatar=self.cleaned_data['avatar'], primary=True).save()
