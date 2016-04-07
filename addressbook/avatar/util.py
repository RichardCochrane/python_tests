import hashlib

from django.core.cache import cache
from django.utils import six
from django.template.defaultfilters import slugify

try:
    from django.utils.encoding import force_bytes
except ImportError:
    force_bytes = str

from avatar.conf import settings

from contacts.models import Contact


cached_funcs = set()


def get_code_name(contact):
    """Return code_name of a Contact instance."""
    return contact.code_name


def get_contact(code_name):
    """Return contact from a code_name."""
    return Contact.objects.get(code_name=code_name)


def get_cache_key(contact_or_code_name, size, prefix):
    """Return a cache key consisten of a code_name and image size."""
    if isinstance(contact_or_code_name, Contact):
        contact_or_code_name = get_code_name(contact_or_code_name)
    key = six.u('%s_%s_%s') % (prefix, contact_or_code_name, size)
    return six.u('%s_%s') % (slugify(key)[:100],
                             hashlib.md5(force_bytes(key)).hexdigest())


def cache_set(key, value):
    cache.set(key, value, settings.AVATAR_CACHE_TIMEOUT)
    return value


def cache_result(default_size=settings.AVATAR_DEFAULT_SIZE):
    """Decorator to cache the result of functions that take a ``contact`` and a ``size`` value."""
    def decorator(func):
        def cached_func(contact, size=None):
            prefix = func.__name__
            cached_funcs.add(prefix)
            key = get_cache_key(contact, size or default_size, prefix=prefix)
            result = cache.get(key)
            if result is None:
                result = func(contact, size or default_size)
                cache_set(key, result)
            return result
        return cached_func
    return decorator


def invalidate_cache(contact, size=None):
    """Function to be called when saving or changing a contact's avatars."""
    sizes = set(settings.AVATAR_AUTO_GENERATE_SIZES)
    if size is not None:
        sizes.add(size)
    for prefix in cached_funcs:
        for size in sizes:
            cache.delete(get_cache_key(contact, size, prefix))


def get_default_avatar_url():
    base_url = getattr(settings, 'STATIC_URL', None)
    if not base_url:
        base_url = getattr(settings, 'MEDIA_URL', '')

    # Don't use base_url if the default url starts with http:// of https://
    if settings.AVATAR_DEFAULT_URL.startswith(('http://', 'https://')):
        return settings.AVATAR_DEFAULT_URL
    # We'll be nice and make sure there are no duplicated forward slashes
    ends = base_url.endswith('/')

    begins = settings.AVATAR_DEFAULT_URL.startswith('/')
    if ends and begins:
        base_url = base_url[:-1]
    elif not ends and not begins:
        return '%s/%s' % (base_url, settings.AVATAR_DEFAULT_URL)

    return '%s%s' % (base_url, settings.AVATAR_DEFAULT_URL)


def get_primary_avatar(contact, size=settings.AVATAR_DEFAULT_SIZE):
    try:
        # Order by -primary first; this means if a primary=True avatar exists
        # it will be first, and then ordered by date uploaded, otherwise a
        # primary=False avatar will be first.  Exactly the fallback behavior we
        # want.
        avatar = contact.avatars.order_by("-primary", "-date_uploaded")[0]
    except IndexError:
        avatar = None
    if avatar:
        if not avatar.thumbnail_exists(size):
            avatar.create_thumbnail(size)
    return avatar
