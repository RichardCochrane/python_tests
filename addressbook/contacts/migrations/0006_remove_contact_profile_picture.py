# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-13 09:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0005_auto_20160213_0909'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='profile_picture',
        ),
    ]
