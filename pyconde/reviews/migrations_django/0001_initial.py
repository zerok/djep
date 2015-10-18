# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.db.models.deletion
import pyconde.tagging
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('speakers', '__first__'),
        ('taggit', '0002_auto_20150616_2121'),
        ('proposals', '0001_initial'),
        ('conference', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('content', models.TextField(verbose_name='content')),
                ('pub_date', models.DateTimeField(verbose_name='publication date', default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(verbose_name='deleted', default=False)),
                ('deleted_date', models.DateTimeField(verbose_name='deleted at', null=True, blank=True)),
                ('deleted_reason', models.TextField(verbose_name='deletion reason', null=True, blank=True)),
                ('author', models.ForeignKey(verbose_name='author', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, verbose_name='deleted by', related_name='deleted_comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
            },
        ),
        migrations.CreateModel(
            name='ProposalMetaData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('num_comments', models.PositiveIntegerField(verbose_name='number of comments', default=0)),
                ('num_reviews', models.PositiveIntegerField(verbose_name='number of reviews', default=0)),
                ('latest_activity_date', models.DateTimeField(verbose_name='latest activity', null=True, blank=True)),
                ('latest_comment_date', models.DateTimeField(verbose_name='latest comment', null=True, blank=True)),
                ('latest_review_date', models.DateTimeField(verbose_name='latest review', null=True, blank=True)),
                ('latest_version_date', models.DateTimeField(verbose_name='latest version', null=True, blank=True)),
                ('score', models.FloatField(verbose_name='score', default=0.0)),
            ],
            options={
                'verbose_name': 'proposal metadata',
                'verbose_name_plural': 'proposal metadata',
            },
        ),
        migrations.CreateModel(
            name='ProposalVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(verbose_name='title', max_length=100)),
                ('description', models.TextField(verbose_name='description', max_length=400)),
                ('abstract', models.TextField(verbose_name='abstract')),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('submission_date', models.DateTimeField(verbose_name='submission date', editable=False, default=django.utils.timezone.now)),
                ('modified_date', models.DateTimeField(verbose_name='modification date', null=True, blank=True)),
                ('language', models.CharField(verbose_name='language', default='de', max_length=5, choices=[('de', 'German'), ('en', 'English')])),
                ('accept_recording', models.BooleanField(default=True)),
                ('pub_date', models.DateTimeField(verbose_name='publication date')),
                ('additional_speakers', models.ManyToManyField(verbose_name='additional speakers', related_name='proposalversion_participations', to='speakers.Speaker', null=True, blank=True)),
                ('audience_level', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='target-audience', to='conference.AudienceLevel')),
                ('available_timeslots', models.ManyToManyField(verbose_name='available timeslots', to='proposals.TimeSlot', null=True, blank=True)),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='conference', to='conference.Conference')),
                ('creator', models.ForeignKey(verbose_name='creator', to=settings.AUTH_USER_MODEL)),
                ('duration', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='duration', to='conference.SessionDuration')),
                ('kind', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='type', to='conference.SessionKind')),
            ],
            options={
                'verbose_name': 'proposal version',
                'verbose_name_plural': 'proposal versions',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('rating', models.CharField(verbose_name='rating', max_length=2, choices=[('-1', '-1'), ('-0', '-0'), ('+0', '+0'), ('+1', '+1')])),
                ('summary', models.TextField(verbose_name='summary')),
                ('pub_date', models.DateTimeField(verbose_name='publication date', default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'review',
                'verbose_name_plural': 'reviews',
            },
        ),
        migrations.CreateModel(
            name='Reviewer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('state', models.PositiveSmallIntegerField(verbose_name='state', default=0, choices=[(0, 'pending request'), (1, 'request accepted'), (2, 'request declined')])),
                ('conference', models.ForeignKey(to='conference.Conference')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'reviewer',
                'verbose_name_plural': 'reviewers',
            },
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('proposals.proposal',),
        ),
        migrations.AddField(
            model_name='review',
            name='proposal',
            field=models.ForeignKey(verbose_name='proposal', related_name='reviews', to='reviews.Proposal'),
        ),
        migrations.AddField(
            model_name='review',
            name='proposal_version',
            field=models.ForeignKey(blank=True, null=True, verbose_name='proposal version', to='reviews.ProposalVersion'),
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='proposalversion',
            name='original',
            field=models.ForeignKey(verbose_name='original proposal', related_name='versions', to='proposals.Proposal'),
        ),
        migrations.AddField(
            model_name='proposalversion',
            name='speaker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='speaker', related_name='proposalversions', to='speakers.Speaker'),
        ),
        migrations.AddField(
            model_name='proposalversion',
            name='tags',
            field=pyconde.tagging.TaggableManager(help_text='A comma-separated list of tags.', blank=True, through='taggit.TaggedItem', verbose_name='Tags', to='taggit.Tag'),
        ),
        migrations.AddField(
            model_name='proposalversion',
            name='track',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, verbose_name='track', to='conference.Track'),
        ),
        migrations.AddField(
            model_name='proposalmetadata',
            name='latest_proposalversion',
            field=models.ForeignKey(blank=True, null=True, verbose_name='latest proposal version', to='reviews.ProposalVersion'),
        ),
        migrations.AddField(
            model_name='proposalmetadata',
            name='proposal',
            field=models.OneToOneField(verbose_name='proposal', related_name='review_metadata', to='reviews.Proposal'),
        ),
        migrations.AddField(
            model_name='comment',
            name='proposal',
            field=models.ForeignKey(verbose_name='proposal', related_name='comments', to='reviews.Proposal'),
        ),
        migrations.AddField(
            model_name='comment',
            name='proposal_version',
            field=models.ForeignKey(blank=True, null=True, verbose_name='proposal version', to='reviews.ProposalVersion'),
        ),
        migrations.AlterUniqueTogether(
            name='reviewer',
            unique_together=set([('conference', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set([('user', 'proposal')]),
        ),
    ]
