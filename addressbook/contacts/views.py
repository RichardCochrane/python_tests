"""Views for processing all Contact requests."""

from django.shortcuts import render, redirect

from contacts.models import Contact
from contacts.forms import ContactForm

from avatar.forms import UploadAvatarForm


def index(request, template_name='contacts/index.html'):
    """View to list all contacts."""
    contacts = Contact.objects.all()
    return render(request, template_name, {'contacts': contacts})


def create_details(request, template_name='contacts/edit_details.html'):
    """View to create a contact by filling in the contact details only."""
    return add_or_update_contact_details(request, template_name, None, "create")


def update_details(request, contact_id, template_name='contacts/edit_details.html'):
    """View to update a contact."""
    contact = Contact.objects.get(id=contact_id)
    return add_or_update_contact_details(request, template_name, contact, "update")


def add_or_update_contact_details(request, template_name, contact, context):
    """
    Either create a new contact or update an existing contacts details.

    request:       the request object passed to the view
    template_name: template to be rendered by this function
    contact:       instance of contact to whom the avatar will be linked - it must exist, even for
                   new contacts
    context:       "create" or "update" depending on how the "template_name" is going to be rendered
    """
    contact_form = ContactForm(request.POST or None, instance=contact)

    if contact_form.is_valid():
        contact = contact_form.save()
        return redirect('contacts:update_contact_avatar', contact_id=contact.id)

    return render(request, template_name, {
        'action': context,
        'contact_form': contact_form
    })


def update_avatar(request, contact_id, template_name='contacts/edit_avatar.html'):
    """View to add a new avatar for a contact."""
    contact = Contact.objects.get(id=contact_id)
    avatar_form = UploadAvatarForm(request.POST or None, request.FILES or None)

    if avatar_form.is_valid():
        avatar_form.save(contact)
        return redirect('contacts:update_contact_powers', contact_id=contact.id)

    return render(request, template_name, {
        'avatar_form': avatar_form,
        'contact': contact
    })


def update_powers(request, contact_id, template_name='contacts/edit_powers.html'):
    """View to update a contact's super-powers."""
    contact = Contact.objects.get(id=contact_id)

    return render(request, template_name, {
        'contact': contact
    })


def delete(request, contact_id):
    """View to delete a contact."""
    Contact.objects.filter(id=contact_id).delete()
    return redirect('index')
