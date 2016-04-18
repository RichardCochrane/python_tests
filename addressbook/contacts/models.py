"""Models required to support all contact details for the address book."""

from __future__ import unicode_literals

from django.db import models

from contacts.lib.contact_grader import Grader


def contact_directory_path(instance, filename):
    """Return the appropriate folder to store an avatar in."""
    # file will be uploaded to MEDIA_ROOT/avatars/contact_<id>/<filename>
    file_extension = filename.split('.')[-1]
    return 'avatars/contact_{0}/{1}.{2}'.format(instance.id, instance.id, file_extension)


class Contact(models.Model):
    """Model class that represents one specific person in the AddressBook."""

    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    nick_name = models.CharField(max_length=40, null=True, blank=True)
    code_name = models.CharField(max_length=40)
    telephone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=80, null=True, blank=True)

    def __str__(self):
        """
        Return superhero name.

        >>> contact = Contact(code_name='DevMan')
        >>> print contact
        u'DevMan'

        >>> contact = Contact(first_name='Richard', last_name='Cochrane')
        >>> str(contact)
        u'(no code name) Richard Cochrane'
        """
        return self.code_name

    @property
    def full_name(self):
        """
        Return combined first and last name to give full name.

        >>> contact = Contact(first_name='Richard', last_name='Cochrane')
        >>> contact.full_name
        u'Richard Cochrane'

        >>> contact.last_name = ''
        >>> contact.full_name
        u'Richard'
        """
        if self.nick_name:
            return '{} "{}" {}'.format(self.first_name, self.nick_name, self.last_name).strip()
        else:
            return '{} {}'.format(self.first_name, self.last_name).strip()

    @property
    def powers(self):
        """Return comma-concatenated list of associated powers."""
        return [p.super_power.power.title() for p in self.super_powers.all()]

    @property
    def avatar(self):
        """Return the primary avatar for the contact (if possible)."""
        if self.avatars.filter(primary=True):
            return self.avatars.filter(primary=True)[0]

        return None

    @property
    def grade(self):
        """
        Return the power grading of the contact.

        >>> contact = Contact()
        >>> contact.grade
        0
        """
        return Grader(self).grade()


class SuperPower(models.Model):
    """Model class that stores possible super-powers."""

    power = models.CharField(max_length=100)

    def __str__(self):
        """Return name of power."""
        return self.power


class ContactSuperPowers(models.Model):
    """Model class that links contacts to specific super-powers."""

    contact = models.ForeignKey(Contact, related_name='super_powers')
    super_power = models.ForeignKey(SuperPower)
