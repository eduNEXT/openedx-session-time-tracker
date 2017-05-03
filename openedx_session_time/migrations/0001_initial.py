# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SessionLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dtcreated', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('username', models.CharField(max_length=32, blank=True)),
                ('courseid', models.TextField(blank=True)),
                ('session_duration', models.DurationField(verbose_name='Session duration')),
                ('start_time', models.DateTimeField(verbose_name='Started at')),
                ('end_time', models.DateTimeField(verbose_name='Ended at')),
                ('host', models.CharField(max_length=64, blank=True)),
            ],
        ),
    ]
