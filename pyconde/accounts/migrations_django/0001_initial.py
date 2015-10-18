# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pyconde.accounts.validators
import taggit.managers
from django.conf import settings
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_auto_20151018_1212'),
        ('schedule', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='BadgeStatus',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='Name', max_length=50)),
                ('slug', models.SlugField(verbose_name='slug')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Status',
                'verbose_name_plural': 'Statuses',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('short_info', models.TextField(verbose_name='short info', blank=True)),
                ('avatar', easy_thumbnails.fields.ThumbnailerImageField(null=True, blank=True, verbose_name='avatar', validators=[pyconde.accounts.validators.avatar_dimension, pyconde.accounts.validators.avatar_format], upload_to='avatars')),
                ('num_accompanying_children', models.PositiveIntegerField(verbose_name='Number of accompanying children', default=0, blank=True, null=True)),
                ('age_accompanying_children', models.CharField(verbose_name='Age of accompanying children', max_length=20, blank=True)),
                ('twitter', models.CharField(verbose_name='Twitter', max_length=20, blank=True, validators=[pyconde.accounts.validators.twitter_username])),
                ('website', models.URLField(verbose_name='Website', blank=True)),
                ('organisation', models.TextField(verbose_name='Organisation', blank=True)),
                ('full_name', models.CharField(verbose_name='Full name', max_length=255, blank=True)),
                ('display_name', models.CharField(verbose_name='Display name', max_length=255, blank=True, help_text='What name should be displayed to other people?')),
                ('addressed_as', models.CharField(verbose_name='Address me as', max_length=255, blank=True, help_text='How should we call you in mails and dialogs throughout the website?')),
                ('accept_pysv_conferences', models.BooleanField(verbose_name='Allow copying to PySV conferences', default=False)),
                ('accept_ep_conferences', models.BooleanField(verbose_name='Allow copying to EPS conferences', default=False)),
                ('accept_job_offers', models.BooleanField(verbose_name='Allow sponsors to send job offers', default=False)),
                ('badge_status', models.ManyToManyField(verbose_name='Badge status', to='accounts.BadgeStatus', blank=True, related_name='profiles')),
                ('sessions_attending', models.ManyToManyField(verbose_name='Trainings', to='schedule.Session', blank=True, related_name='attendees')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', blank=True, verbose_name='Tags')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='profile')),
            ],
            options={
                'permissions': (('send_user_mails', 'Allow sending mails to users through the website'), ('export_guidebook', 'Allow export of guidebook data'), ('see_checkin_info', 'Allow seeing check-in information'), ('perform_purchase', 'Allow performing purchases')),
            },
        ),
        migrations.CreateModel(
            name='UserListPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(serialize=False, to='cms.CMSPlugin', auto_created=True, primary_key=True, parent_link=True)),
                ('additional_names', models.TextField(verbose_name='Additional names', default='', help_text='Users without account. One name per line.', blank=True)),
                ('badge_status', models.ManyToManyField(verbose_name='Status', to='accounts.BadgeStatus', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
