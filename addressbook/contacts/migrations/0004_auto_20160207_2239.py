# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-07 22:39
from __future__ import unicode_literals

import os

import contacts.models
from django.conf import settings
from django.core.files import File
from django.db import migrations, models


def add_avatars(apps, schema_editor):
    Contact = apps.get_model('contacts', 'Contact')

    png_avatars = ['mystique', 'rogue']
    for contact in Contact.objects.all():
        avatar_source_path = os.path.join(
            settings.BASE_DIR, 'addressbook', 'site_media', 'static', 'images', 'source')
        code_name = contact.code_name.lower()
        avatar_filename = '{}.{}'.format(code_name, 'png' if code_name in png_avatars else 'jpg')

        contact_avatar = File(open('{}/{}'.format(avatar_source_path, avatar_filename), 'r'))
        contact.avatar.save(avatar_filename, contact_avatar, save=True)


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0003_auto_20160206_2144'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=contacts.models.contact_directory_path),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='telephone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.RunPython(add_avatars)
    ]