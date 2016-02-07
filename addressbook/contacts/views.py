"""Views for processing all Contact requests."""

from contacts.models import Contact

from django.shortcuts import render


def index(request, template_name='contacts/index.html'):
    """View to list all contacts."""
    contacts = Contact.objects.all()

    return render(request, template_name, {'contacts': contacts})


def create(request, template_name='contacts/edit.html'):
    """View to create a contact."""
    pass


def update(request, contact_id, template_name='contacts/edit.html'):
    """View to update a contact."""
    pass


def delete(request, contact_id):
    """View to delete a contact."""
    pass
