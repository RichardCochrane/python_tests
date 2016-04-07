import hashlib

try:
    from urllib.parse import urljoin, urlencode
except ImportError:
    from urlparse import urljoin
    from urllib import urlencode

from django import template
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils import six
from django.utils.translation import ugettext as _

from avatar.conf import settings
from avatar.util import get_primary_avatar, get_default_avatar_url, cache_result, get_contact, \
    force_bytes
from avatar.models import Avatar

from contacts.models import Contact

register = template.Library()


@cache_result()
@register.simple_tag
def avatar_url(contact, size=settings.AVATAR_DEFAULT_SIZE):
    avatar = get_primary_avatar(contact, size=size)

    if avatar:
        return avatar.avatar_url(size)

    if settings.AVATAR_GRAVATAR_BACKUP:
        params = {'s': str(size)}
        if settings.AVATAR_GRAVATAR_DEFAULT:
            params['d'] = settings.AVATAR_GRAVATAR_DEFAULT
        path = "%s/?%s" % (hashlib.md5(force_bytes(
            getattr(contact, settings.AVATAR_GRAVATAR_FIELD))).hexdigest(), urlencode(params))
        return urljoin(settings.AVATAR_GRAVATAR_BASE_URL, path)

    return get_default_avatar_url()


@register.simple_tag
def avatar(contact, size=settings.AVATAR_DEFAULT_SIZE, **kwargs):

    if not isinstance(contact, Contact):
        try:
            contact = get_contact(contact)
            alt = six.text_type(contact)
            url = avatar_url(contact, size)
        except Contact.DoesNotExist:
            url = get_default_avatar_url()
            alt = _("Default Avatar")
    else:
        alt = six.text_type(contact)
        url = avatar_url(contact, size)
    context = dict(kwargs, **{
        'contact': contact,
        'url': url,
        'alt': alt,
        'size': size,
    })
    return render_to_string('avatar/avatar_tag.html', context)


@register.filter
def has_avatar(contact):
    if not isinstance(contact, Contact):
        return False
    return Avatar.objects.filter(contact=contact, primary=True).exists()


@cache_result()
@register.simple_tag
def primary_avatar(contact, size=settings.AVATAR_DEFAULT_SIZE):
    """
    This tag tries to get the default avatar for a contact without doing any db
    requests. It achieve this by linking to a special view that will do all the
    work for us. If that special view is then cached by a CDN for instance,
    we will avoid many db calls.
    """
    alt = six.text_type(contact)
    url = reverse('avatar_render_primary', kwargs={'contact': contact, 'size': size})
    return ("""<img src="%s" alt="%s" width="%s" height="%s" />""" %
            (url, alt, size, size))


@cache_result()
@register.simple_tag
def render_avatar(avatar, size=settings.AVATAR_DEFAULT_SIZE):
    if not avatar.thumbnail_exists(size):
        avatar.create_thumbnail(size)
    return """<img src="%s" alt="%s" width="%s" height="%s" />""" % (
        avatar.avatar_url(size), six.text_type(avatar), size, size)


@register.tag
def primary_avatar_object(parser, token):
    split = token.split_contents()
    if len(split) == 4:
        return ContactsAvatarObjectNode(split[1], split[3])
    raise template.TemplateSyntaxError('%r tag takes three arguments.' % split[0])


class ContactsAvatarObjectNode(template.Node):
    def __init__(self, contact, key):
        self.contact = template.Variable(contact)
        self.key = key

    def render(self, context):
        contact = self.contact.resolve(context)
        key = self.key
        avatar = Avatar.objects.filter(contact=contact, primary=True)
        if avatar:
            context[key] = avatar[0]
        else:
            context[key] = None
        return six.text_type()
