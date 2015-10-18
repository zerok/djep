# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_auto_20151018_1212'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestimonialCollectionPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, to='cms.CMSPlugin', serialize=False, primary_key=True, parent_link=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='TestimonialPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, to='cms.CMSPlugin', serialize=False, primary_key=True, parent_link=True)),
                ('content', models.TextField(verbose_name='content')),
                ('author', models.CharField(max_length=255, verbose_name='author')),
                ('author_image', models.ImageField(upload_to='testimonials', verbose_name="author's photo")),
                ('author_url', models.URLField(null=True, verbose_name="author's website", blank=True)),
                ('author_description', models.CharField(verbose_name="author's description", max_length=100, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
