# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('speakers', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='LightningTalk',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('slides_url', models.URLField(blank=True, null=True, verbose_name='slides URL')),
                ('speakers', sortedm2m.fields.SortedManyToManyField(help_text=None, to='speakers.Speaker', null=True, blank=True, related_name='lightning_talks', verbose_name='speakers')),
            ],
        ),
    ]
