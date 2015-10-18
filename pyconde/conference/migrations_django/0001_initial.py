# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AudienceLevel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('level', models.IntegerField(blank=True, null=True, verbose_name='level')),
            ],
            options={
                'verbose_name_plural': 'target-audiences',
                'verbose_name': 'target-audience',
                'ordering': ['level'],
            },
        ),
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('slug', models.SlugField(blank=True, null=True, verbose_name='slug')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='start date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='end date')),
                ('reviews_start_date', models.DateTimeField(blank=True, null=True)),
                ('reviews_end_date', models.DateTimeField(blank=True, null=True)),
                ('reviews_active', models.NullBooleanField()),
                ('tickets_editable', models.BooleanField(default=True)),
                ('tickets_editable_until', models.DateTimeField(blank=True, null=True)),
                ('anonymize_proposal_author', models.BooleanField(default=True, verbose_name='anonymize proposal author')),
            ],
            options={
                'verbose_name_plural': 'conferences',
                'verbose_name': 'conference',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('order', models.IntegerField(default=0, verbose_name='order')),
                ('used_for_sessions', models.BooleanField(default=True, verbose_name='used for sessions')),
                ('conference', models.ForeignKey(to='conference.Conference', verbose_name='conference')),
            ],
            options={
                'verbose_name_plural': 'locations',
                'verbose_name': 'location',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='start date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='end date')),
                ('slug', models.SlugField(blank=True, null=True, verbose_name='slug')),
                ('order', models.IntegerField(default=0, verbose_name='order')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('conference', models.ForeignKey(related_name='sections', verbose_name='conference', to='conference.Conference')),
            ],
            options={
                'verbose_name_plural': 'sections',
                'verbose_name': 'section',
            },
        ),
        migrations.CreateModel(
            name='SessionDuration',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('label', models.CharField(max_length=100, verbose_name='label')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('minutes', models.IntegerField(verbose_name='minutes')),
                ('conference', models.ForeignKey(to='conference.Conference', verbose_name='conference')),
            ],
            options={
                'verbose_name_plural': 'session durations',
                'verbose_name': 'session duration',
            },
        ),
        migrations.CreateModel(
            name='SessionKind',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('closed', models.NullBooleanField()),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('conference', models.ForeignKey(to='conference.Conference', verbose_name='conference')),
                ('sections', models.ManyToManyField(to='conference.Section', verbose_name='section')),
            ],
            options={
                'verbose_name_plural': 'session types',
                'verbose_name': 'session type',
                'ordering': ('start_date', 'end_date', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('visible', models.BooleanField(default=True, verbose_name='visible')),
                ('order', models.IntegerField(default=0, verbose_name='order')),
                ('conference', models.ForeignKey(to='conference.Conference', verbose_name='conference')),
            ],
            options={
                'verbose_name_plural': 'tracks',
                'verbose_name': 'track',
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='audiencelevel',
            name='conference',
            field=models.ForeignKey(to='conference.Conference', verbose_name='conference'),
        ),
    ]
