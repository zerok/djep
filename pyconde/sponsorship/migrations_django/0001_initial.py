# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0001_initial'),
        ('cms', '0013_auto_20151018_1212'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobOffer',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(verbose_name='Title', max_length=255)),
                ('text', models.TextField(verbose_name='Text')),
                ('link', models.URLField(verbose_name='URL')),
                ('active', models.BooleanField(verbose_name='Active', default=False)),
                ('added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Job offer',
                'verbose_name_plural': 'Job offers',
                'ordering': ('sponsor__level__order', '-added'),
            },
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='name', max_length=100)),
                ('external_url', models.URLField(verbose_name='external URL')),
                ('annotation', models.TextField(verbose_name='annotation', blank=True)),
                ('description', models.TextField(verbose_name='description', blank=True, null=True)),
                ('contact_name', models.CharField(verbose_name='contact_name', blank=True, null=True, max_length=100)),
                ('contact_email', models.EmailField(verbose_name='Contact e‑mail', blank=True, null=True, max_length=254)),
                ('logo', models.ImageField(verbose_name='logo', upload_to='sponsor_logos/')),
                ('added', models.DateTimeField(verbose_name='added', default=django.utils.timezone.now)),
                ('active', models.BooleanField(verbose_name='active', default=False)),
                ('custom_logo_size_listing', models.CharField(help_text='Format: [width]x[height]. To get the maximum height out of a logo, use something like 300x55.', verbose_name='Custom logo size in listings', blank=True, null=True, max_length=9)),
            ],
            options={
                'verbose_name': 'sponsor',
                'verbose_name_plural': 'sponsors',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SponsorLevel',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='name', max_length=100)),
                ('order', models.IntegerField(verbose_name='order', default=0)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('slug', models.SlugField(verbose_name='slug')),
                ('conference', models.ForeignKey(verbose_name='conference', to='conference.Conference')),
            ],
            options={
                'verbose_name': 'sponsor level',
                'verbose_name_plural': 'sponsor levels',
                'ordering': ['conference', 'order'],
            },
        ),
        migrations.CreateModel(
            name='SponsorListPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(serialize=False, to='cms.CMSPlugin', parent_link=True, primary_key=True, auto_created=True)),
                ('title', models.CharField(verbose_name='title', blank=True, max_length=100)),
                ('group', models.BooleanField(verbose_name='group by level', default=False)),
                ('split_list_length', models.IntegerField(verbose_name='length of split splits', blank=True, default=None, null=True)),
                ('custom_css_classes', models.CharField(help_text='Use slides-2rows if your row actually consists of two rows.', verbose_name='custom CSS classes', blank=True, max_length=100)),
                ('levels', models.ManyToManyField(verbose_name='sponsor levels', to='sponsorship.SponsorLevel')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='level',
            field=models.ForeignKey(verbose_name='level', to='sponsorship.SponsorLevel'),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='sponsor',
            field=models.ForeignKey(verbose_name='sponsor', to='sponsorship.Sponsor'),
        ),
    ]
