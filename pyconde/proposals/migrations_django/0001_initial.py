# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import pyconde.tagging
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0001_initial'),
        ('speakers', '__first__'),
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(verbose_name='title', max_length=100)),
                ('description', models.TextField(verbose_name='description', max_length=400)),
                ('abstract', models.TextField(verbose_name='abstract')),
                ('notes', models.TextField(blank=True, verbose_name='notes')),
                ('submission_date', models.DateTimeField(editable=False, verbose_name='submission date', default=django.utils.timezone.now)),
                ('modified_date', models.DateTimeField(null=True, blank=True, verbose_name='modification date')),
                ('language', models.CharField(verbose_name='language', default='de', max_length=5, choices=[('de', 'German'), ('en', 'English')])),
                ('accept_recording', models.BooleanField(default=True)),
                ('additional_speakers', models.ManyToManyField(null=True, blank=True, to='speakers.Speaker', verbose_name='additional speakers', related_name='proposal_participations')),
                ('audience_level', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='target-audience', to='conference.AudienceLevel')),
            ],
            options={
                'permissions': (('see_proposal_author', 'Can always see the proposal author'),),
                'verbose_name': 'proposal',
                'verbose_name_plural': 'proposals',
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('date', models.DateField(verbose_name='date')),
                ('slot', models.IntegerField(verbose_name='timeslot', choices=[(1, 'morning'), (2, 'afternoon')])),
                ('section', models.ForeignKey(verbose_name='section', to='conference.Section')),
            ],
            options={
                'verbose_name': 'timeslot',
                'verbose_name_plural': 'timeslots',
                'ordering': ('date',),
            },
        ),
        migrations.AddField(
            model_name='proposal',
            name='available_timeslots',
            field=models.ManyToManyField(null=True, blank=True, verbose_name='available timeslots', to='proposals.TimeSlot'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='conference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='conference', to='conference.Conference'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='duration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='duration', to='conference.SessionDuration'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='kind',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='type', to='conference.SessionKind'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='speaker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='speaker', to='speakers.Speaker', related_name='proposals'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='tags',
            field=pyconde.tagging.TaggableManager(through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags', blank=True, to='taggit.Tag'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='track',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.PROTECT, verbose_name='track', to='conference.Track'),
        ),
        migrations.AlterUniqueTogether(
            name='timeslot',
            unique_together=set([('date', 'slot', 'section')]),
        ),
    ]
