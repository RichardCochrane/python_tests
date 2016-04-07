from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils import six
from django.template.loader import render_to_string

from avatar.models import Avatar


class AvatarAdmin(admin.ModelAdmin):
    list_display = ('get_avatar', 'contact', 'primary', "date_uploaded")
    list_filter = ('primary',)
    search_fields = ('contact__codename',)
    list_per_page = 50

    def get_avatar(self, avatar_in):
        context = dict({
            'contact': avatar_in.contact,
            'url': avatar_in.avatar.url,
            'alt': six.text_type(avatar_in.contact),
            'size': 80,
        })
        return render_to_string('avatar/avatar_tag.html', context)

    get_avatar.short_description = _('Avatar')
    get_avatar.allow_tags = True


admin.site.register(Avatar, AvatarAdmin)
