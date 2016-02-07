"""Models required to support all contact details for the address book."""

from __future__ import unicode_literals

from django.db import models


class Contact(models.Model):
    """Model class that represents one specific person in the AddressBook."""

    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    nick_name = models.CharField(max_length=40, null=True, blank=True)
    code_name = models.CharField(max_length=40)
    telephone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=20, null=True, blank=True)

    def __str__(self):
        """Return superhero name."""
        return self.code_name

    @property
    def full_name(self):
        """Return combined first and last name to give full name."""
        if self.nick_name:
            return '{} "{}" {}'.format(self.first_name, self.nick_name, self.last_name).strip()
        else:
            return '{} {}'.format(self.first_name, self.last_name).strip()


class SuperPower(models.Model):
    """Model class that stores possible super-powers."""

    power = models.CharField(max_length=100)


class ContactSuperPowers(models.Model):
    """Model class that links contacts to specific super-powers."""

    contact = models.ForeignKey(Contact)
    super_power = models.ForeignKey(SuperPower)
