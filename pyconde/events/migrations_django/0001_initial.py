# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('date', models.DateTimeField(verbose_name='Date')),
                ('end_date', models.DateTimeField(blank=True, verbose_name='End date', null=True)),
                ('link', models.URLField(blank=True, verbose_name='Link', null=True)),
                ('conference', models.ForeignKey(to='conference.Conference', verbose_name='Conference')),
            ],
            options={
                'verbose_name_plural': 'events',
                'ordering': ['date'],
                'verbose_name': 'event',
            },
        ),
    ]
