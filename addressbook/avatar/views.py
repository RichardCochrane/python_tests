from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from avatar.conf import settings
from avatar.forms import UploadAvatarForm
from avatar.models import Avatar
from avatar.signals import avatar_updated
from avatar.util import (get_primary_avatar, get_default_avatar_url, get_contact)

from contacts.models import Contact


def _get_next(request):
    """
    The part that's the least straightforward about views in this module is
    how they determine their redirects after they have finished computation.

    In short, they will try and determine the next place to go in the
    following order:

    1. If there is a variable named ``next`` in the *POST* parameters, the
       view will redirect to that variable's value.
    2. If there is a variable named ``next`` in the *GET* parameters,
       the view will redirect to that variable's value.
    3. If Django can determine the previous page from the HTTP headers,
       the view will redirect to that previous page.
    """
    next = request.POST.get('next', request.GET.get('next',
                            request.META.get('HTTP_REFERER', None)))
    if not next:
        next = request.path
    return next


def _get_avatars(contact):
    # Default set. Needs to be sliced, but that's it. Keep the natural order.
    avatars = contact.avatar_set.all()

    # Current avatar
    primary_avatar = avatars.order_by('-primary')[:1]
    if primary_avatar:
        avatar = primary_avatar[0]
    else:
        avatar = None

    if settings.AVATAR_MAX_AVATARS_PER_USER == 1:
        avatars = primary_avatar
    else:
        # Slice the default set now that we used
        # the queryset for the primary avatar
        avatars = avatars[:settings.AVATAR_MAX_AVATARS_PER_USER]
    return (avatar, avatars)


@login_required
def add(request, extra_context=None, next_override=None,
        upload_form=UploadAvatarForm, *args, **kwargs):
    if extra_context is None:
        extra_context = {}
    avatar, avatars = _get_avatars(request.user)
    upload_avatar_form = upload_form(request.POST or None,
                                     request.FILES or None,
                                     user=request.user)
    if request.method == "POST" and 'avatar' in request.FILES:
        if upload_avatar_form.is_valid():
            avatar = Avatar(user=request.user, primary=True)
            image_file = request.FILES['avatar']
            avatar.avatar.save(image_file.name, image_file)
            avatar.save()
            messages.success(request, _("Successfully uploaded a new avatar."))
            avatar_updated.send(sender=Avatar, user=request.user, avatar=avatar)
            return redirect(next_override or _get_next(request))
    context = {
        'avatar': avatar,
        'avatars': avatars,
        'upload_avatar_form': upload_avatar_form,
        'next': next_override or _get_next(request),
    }
    context.update(extra_context)
    return render(request, 'avatar/add.html', context)


def avatar(request, codename, id, template_name="avatar/avatar.html"):
    try:
        contact = get_contact(codename)
    except Contact.DoesNotExist:
        raise Http404
    avatars = contact.avatar_set.order_by("-date_uploaded")
    index = None
    avatar = None
    if avatars:
        avatar = avatars.get(pk=id)
        if not avatar:
            return Http404

        index = avatars.filter(date_uploaded__gt=avatar.date_uploaded).count()
        count = avatars.count()

        if index == 0:
            prev = avatars.reverse()[0]
            if count <= 1:
                next = avatars[0]
            else:
                next = avatars[1]
        else:
            prev = avatars[index - 1]

        if (index + 1) >= count:
            next = avatars[0]
            prev_index = index - 1
            if prev_index < 0:
                prev_index = 0
            prev = avatars[prev_index]
        else:
            next = avatars[index + 1]

    return render(request, template_name, {
        "other_user": contact,
        "avatar": avatar,
        "index": index + 1,
        "avatars": avatars,
        "next": next,
        "prev": prev,
        "count": count,
    })


def render_primary(request, contact=None, size=settings.AVATAR_DEFAULT_SIZE):
    size = int(size)
    avatar = get_primary_avatar(contact, size=size)
    if avatar:
        # FIXME: later, add an option to render the resized avatar dynamically
        # instead of redirecting to an already created static file. This could
        # be useful in certain situations, particulary if there is a CDN and
        # we want to minimize the storage usage on our static server, letting
        # the CDN store those files instead
        url = avatar.avatar_url(size)
    else:
        url = get_default_avatar_url()

    return redirect(url)
