# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-23 16:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bodhibuddyapp', '0004_auto_20161023_1522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shareddaimokusessionentry',
            name='contributor',
        ),
        migrations.DeleteModel(
            name='SharedDaimokuSessionEntry',
        ),
    ]
