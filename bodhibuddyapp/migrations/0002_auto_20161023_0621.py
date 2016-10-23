# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-23 06:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bodhibuddyapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shareddaimokusessionentry',
            name='contributor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='session_user', to='bodhibuddyapp.UserProfile'),
        ),
        migrations.AlterField(
            model_name='shareddaimokutarget',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_user', to='bodhibuddyapp.UserProfile'),
        ),
    ]