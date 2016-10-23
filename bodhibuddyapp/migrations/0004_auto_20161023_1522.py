# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-23 15:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bodhibuddyapp', '0003_auto_20161023_0623'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.TextField(blank=True, max_length=500)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('current_state', models.CharField(choices=[(b'OI', b'OnlineIdle'), (b'OC', b'OnlineChanting'), (b'OF', b'Offline')], default=b'OF', max_length=2)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.AlterField(
            model_name='shareddaimokusessionentry',
            name='contributor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='session_user', to='bodhibuddyapp.Profile'),
        ),
        migrations.AlterField(
            model_name='shareddaimokutarget',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_user', to='bodhibuddyapp.Profile'),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
