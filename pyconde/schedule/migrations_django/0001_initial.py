# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import pyconde.tagging
import django.db.models.deletion
import pyconde.schedule.models
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '__first__'),
        ('proposals', '__first__'),
        ('cms', '0013_auto_20151018_1212'),
        ('lightningtalks', '__first__'),
        ('speakers', '__first__'),
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompleteSchedulePlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(to='cms.CMSPlugin', serialize=False, auto_created=True, primary_key=True, parent_link=True)),
                ('title', models.CharField(blank=True, max_length=100, verbose_name='title')),
                ('row_duration', models.IntegerField(default=15, choices=[(15, '15 Minutes'), (30, '30 Minutes'), (45, '45 Minutes'), (60, '60 Minutes')], verbose_name='Duration of one row')),
                ('merge_sections', models.BooleanField(default=False, verbose_name='Merge different section into same table')),
                ('sections', models.ManyToManyField(blank=True, to='conference.Section', null=True, verbose_name='sections')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('description', models.TextField(max_length=400, verbose_name='description')),
                ('abstract', models.TextField(verbose_name='abstract')),
                ('notes', models.TextField(blank=True, verbose_name='notes')),
                ('submission_date', models.DateTimeField(editable=False, default=django.utils.timezone.now, verbose_name='submission date')),
                ('modified_date', models.DateTimeField(blank=True, null=True, verbose_name='modification date')),
                ('language', models.CharField(default='de', max_length=5, choices=[('de', 'German'), ('en', 'English')], verbose_name='language')),
                ('accept_recording', models.BooleanField(default=True)),
                ('start', models.DateTimeField(blank=True, null=True, verbose_name='start time')),
                ('end', models.DateTimeField(blank=True, null=True, verbose_name='end time')),
                ('is_global', models.BooleanField(default=False, verbose_name='is global')),
                ('released', models.BooleanField(default=False, verbose_name='released')),
                ('slides_url', models.URLField(blank=True, null=True, verbose_name='Slides URL')),
                ('video_url', models.URLField(blank=True, null=True, verbose_name='Video URL')),
                ('max_attendees', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Max attendees')),
                ('additional_speakers', models.ManyToManyField(related_name='session_participations', blank=True, to='speakers.Speaker', null=True, verbose_name='additional speakers')),
                ('audience_level', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='target-audience', to='conference.AudienceLevel')),
                ('available_timeslots', models.ManyToManyField(blank=True, to='proposals.TimeSlot', null=True, verbose_name='available timeslots')),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='conference', to='conference.Conference')),
                ('duration', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='duration', to='conference.SessionDuration')),
                ('kind', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='type', to='conference.SessionKind')),
                ('location', models.ManyToManyField(blank=True, to='conference.Location', null=True, verbose_name='location')),
                ('proposal', models.ForeignKey(blank=True, null=True, verbose_name='proposal', to='proposals.Proposal', related_name='session')),
                ('section', models.ForeignKey(blank=True, null=True, verbose_name='section', to='conference.Section', related_name='sessions')),
                ('speaker', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='speaker', to='speakers.Speaker', related_name='sessions')),
                ('tags', pyconde.tagging.TaggableManager(blank=True, through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags', to='taggit.Tag')),
                ('track', models.ForeignKey(blank=True, null=True, verbose_name='track', to='conference.Track', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name_plural': 'sessions',
                'verbose_name': 'session',
            },
            bases=(pyconde.schedule.models.LocationMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SideEvent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('start', models.DateTimeField(verbose_name='start time')),
                ('end', models.DateTimeField(verbose_name='end time')),
                ('is_global', models.BooleanField(default=False, verbose_name='is global')),
                ('is_pause', models.BooleanField(default=False, verbose_name='is break')),
                ('is_recordable', models.BooleanField(default=False, verbose_name='is recordable')),
                ('icon', models.CharField(choices=[('coffee', 'Coffee cup'), ('glass', 'Glass'), ('lightbulb-o', 'Lightbulb'), ('moon-o', 'Moon'), ('cutlery', 'Cutlery')], blank=True, max_length=50, null=True, verbose_name='icon')),
                ('video_url', models.URLField(blank=True, null=True, verbose_name='Video URL')),
                ('conference', models.ForeignKey(to='conference.Conference', verbose_name='conference')),
                ('lightning_talks', sortedm2m.fields.SortedManyToManyField(help_text=None, blank=True, to='lightningtalks.LightningTalk', null=True)),
                ('location', models.ManyToManyField(blank=True, to='conference.Location', null=True, verbose_name='location')),
                ('section', models.ForeignKey(blank=True, null=True, verbose_name='section', to='conference.Section', related_name='side_events')),
            ],
            bases=(pyconde.schedule.models.LocationMixin, models.Model),
        ),
    ]
