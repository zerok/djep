# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
import pyconde.attendees.validators


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('sponsorship', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conference', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='DietaryPreference',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='Name', unique=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('company_name', models.CharField(verbose_name='Company', max_length=100, blank=True)),
                ('first_name', models.CharField(verbose_name='First name', max_length=250)),
                ('last_name', models.CharField(verbose_name='Last name', max_length=250)),
                ('email', models.EmailField(verbose_name='E-mail', max_length=254)),
                ('street', models.CharField(verbose_name='Street and house number', max_length=100)),
                ('zip_code', models.CharField(verbose_name='Zip code', max_length=20)),
                ('city', models.CharField(verbose_name='City', max_length=100)),
                ('country', models.CharField(verbose_name='Country', max_length=100)),
                ('vat_id', models.CharField(verbose_name='VAT-ID', max_length=16, blank=True)),
                ('date_added', models.DateTimeField(verbose_name='Date (added)', default=django.utils.timezone.now)),
                ('state', models.CharField(verbose_name='Status', default='incomplete', choices=[('incomplete', 'Purchase incomplete'), ('new', 'new'), ('invoice_created', 'invoice created'), ('payment_received', 'payment received'), ('canceled', 'canceled')], max_length=25)),
                ('comments', models.TextField(verbose_name='Comments', blank=True)),
                ('payment_method', models.CharField(verbose_name='Payment method', default='invoice', choices=[('invoice', 'Invoice'), ('creditcard', 'Credit card'), ('elv', 'ELV')], max_length=20)),
                ('payment_transaction', models.CharField(verbose_name='Transaction ID', max_length=255, blank=True)),
                ('payment_total', models.FloatField(verbose_name='Payment total', null=True, blank=True)),
                ('exported', models.BooleanField(verbose_name='Exported', default=False)),
                ('invoice_number', models.IntegerField(verbose_name='Invoice number', null=True, blank=True)),
                ('invoice_filename', models.CharField(verbose_name='Invoice filename', null=True, max_length=255, blank=True)),
                ('conference', models.ForeignKey(verbose_name='conference', to='conference.Conference', null=True, on_delete=django.db.models.deletion.PROTECT)),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Purchase',
                'verbose_name_plural': 'Purchases',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('date_added', models.DateTimeField(verbose_name='Date (added)', default=django.utils.timezone.now)),
                ('canceled', models.BooleanField(verbose_name='Canceled', default=False)),
            ],
            options={
                'ordering': ('ticket_type__tutorial_ticket', 'ticket_type__product_number'),
            },
        ),
        migrations.CreateModel(
            name='TicketType',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('product_number', models.IntegerField(verbose_name='Product number', help_text='Will be created when you save the first time.', blank=True)),
                ('name', models.CharField(verbose_name='Name', max_length=50)),
                ('fee', models.FloatField(verbose_name='Fee', default=0)),
                ('max_purchases', models.PositiveIntegerField(verbose_name='Max. purchases', help_text='0 means no limit', default=0)),
                ('is_active', models.BooleanField(verbose_name='Is active', default=False)),
                ('is_on_desk_active', models.BooleanField(verbose_name='Allow on desk purchase', default=False)),
                ('date_valid_from', models.DateTimeField(verbose_name='Sale start')),
                ('date_valid_to', models.DateTimeField(verbose_name='Sale end')),
                ('valid_on', models.DateField(verbose_name='Valid on', validators=[pyconde.attendees.validators.during_conference], null=True, blank=True)),
                ('tutorial_ticket', models.BooleanField(verbose_name='Tutorial ticket', default=False)),
                ('remarks', models.TextField(verbose_name='Remarks', blank=True)),
                ('allow_editing', models.NullBooleanField(verbose_name='Allow editing')),
                ('editable_fields', models.TextField(verbose_name='Editable fields', blank=True)),
                ('editable_until', models.DateTimeField(verbose_name='Editable until', null=True, blank=True)),
                ('prevent_invoice', models.BooleanField(verbose_name='Conditionally prevent invoice to user', help_text='If checked, a purchase, that contains only tickets of ticket types where this is checked, will not be send to the user. This can be useful for e.g. sponsor tickets', default=False)),
                ('conference', models.ForeignKey(verbose_name='conference', to='conference.Conference', null=True, on_delete=django.db.models.deletion.PROTECT)),
                ('content_type', models.ForeignKey(verbose_name='Ticket to generate', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Ticket type',
                'verbose_name_plural': 'Ticket type',
                'ordering': ('tutorial_ticket', 'product_number', 'vouchertype_needed'),
            },
        ),
        migrations.CreateModel(
            name='TShirtSize',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('size', models.CharField(verbose_name='Size', max_length=100)),
                ('sort', models.IntegerField(verbose_name='Sort order', default=999)),
                ('conference', models.ForeignKey(verbose_name='conference', to='conference.Conference', null=True, on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'T-Shirt size',
                'verbose_name_plural': 'T-Shirt sizes',
                'ordering': ('sort',),
            },
        ),
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('code', models.CharField(verbose_name='Code', help_text='Can be left blank, code will be created when you save.', max_length=12, blank=True)),
                ('remarks', models.CharField(verbose_name='Remarks', max_length=254, blank=True)),
                ('date_valid', models.DateTimeField(verbose_name='Date (valid)', help_text='The voucher is valid until this date')),
                ('is_used', models.BooleanField(verbose_name='Is used', default=False)),
            ],
            options={
                'verbose_name': 'Voucher',
                'verbose_name_plural': 'Vouchers',
            },
        ),
        migrations.CreateModel(
            name='VoucherType',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='voucher type', max_length=50)),
                ('conference', models.ForeignKey(verbose_name='conference', to='conference.Conference', null=True, on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'voucher type',
                'verbose_name_plural': 'voucher types',
            },
        ),
        migrations.CreateModel(
            name='SIMCardTicket',
            fields=[
                ('ticket_ptr', models.OneToOneField(to='attendees.Ticket', serialize=False, primary_key=True, parent_link=True, auto_created=True)),
                ('first_name', models.CharField(verbose_name='First name', max_length=250)),
                ('last_name', models.CharField(verbose_name='Last name', max_length=250)),
                ('date_of_birth', models.DateField(verbose_name='Date of birth')),
                ('gender', models.CharField(verbose_name='Gender', choices=[('female', 'female'), ('male', 'male')], max_length=6)),
                ('hotel_name', models.CharField(verbose_name='Host', help_text='Name of your hotel or host for your stay.', max_length=100, blank=True)),
                ('email', models.EmailField(verbose_name='E-mail', max_length=254)),
                ('street', models.CharField(verbose_name='Street and house number of host', max_length=100)),
                ('zip_code', models.CharField(verbose_name='Zip code of host', max_length=20)),
                ('city', models.CharField(verbose_name='City of host', max_length=100)),
                ('country', models.CharField(verbose_name='Country of host', max_length=100)),
                ('phone', models.CharField(verbose_name='Host phone number', help_text='Please supply the phone number of your hotel or host.', max_length=100)),
                ('sim_id', models.CharField(verbose_name='IMSI', help_text='The IMSI of the SIM Card associated with this account.', max_length=20, blank=True)),
            ],
            options={
                'verbose_name': 'SIM Card',
                'verbose_name_plural': 'SIM Cards',
            },
            bases=('attendees.ticket',),
        ),
        migrations.CreateModel(
            name='SupportTicket',
            fields=[
                ('ticket_ptr', models.OneToOneField(to='attendees.Ticket', serialize=False, primary_key=True, parent_link=True, auto_created=True)),
            ],
            options={
                'verbose_name': 'Support Ticket',
                'verbose_name_plural': 'Support Tickets',
            },
            bases=('attendees.ticket',),
        ),
        migrations.CreateModel(
            name='VenueTicket',
            fields=[
                ('ticket_ptr', models.OneToOneField(to='attendees.Ticket', serialize=False, primary_key=True, parent_link=True, auto_created=True)),
                ('first_name', models.CharField(verbose_name='First name', max_length=250, blank=True)),
                ('last_name', models.CharField(verbose_name='Last name', max_length=250, blank=True)),
                ('organisation', models.CharField(verbose_name='Organization', max_length=100, blank=True)),
                ('dietary_preferences', models.ManyToManyField(verbose_name='Dietary preferences', to='attendees.DietaryPreference', null=True, blank=True)),
                ('shirtsize', models.ForeignKey(verbose_name='Desired T-Shirt size', to='attendees.TShirtSize', null=True, blank=True)),
                ('sponsor', models.ForeignKey(verbose_name='Sponsor', to='sponsorship.Sponsor', null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Conference Ticket',
                'verbose_name_plural': 'Conference Tickets',
            },
            bases=('attendees.ticket',),
        ),
        migrations.AddField(
            model_name='voucher',
            name='type',
            field=models.ForeignKey(verbose_name='voucher type', to='attendees.VoucherType', null=True),
        ),
        migrations.AddField(
            model_name='tickettype',
            name='vouchertype_needed',
            field=models.ForeignKey(verbose_name='voucher type needed', to='attendees.VoucherType', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='purchase',
            field=models.ForeignKey(to='attendees.Purchase'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_type',
            field=models.ForeignKey(verbose_name='Ticket type', to='attendees.TicketType'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='attendees_ticket_tickets', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='venueticket',
            name='voucher',
            field=models.ForeignKey(verbose_name='Voucher', to='attendees.Voucher', null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='tickettype',
            unique_together=set([('product_number', 'conference')]),
        ),
    ]
