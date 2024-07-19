# Generated by Django 5.0.2 on 2024-07-19 07:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, default='')),
                ('recurring', models.BooleanField(default=False)),
                ('max_volunteers', models.IntegerField(default=1)),
                ('start_date', models.DateTimeField()),
                ('duration', models.DurationField(default=2)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.organization')),
                ('shift_manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='shift_managed_events', to=settings.AUTH_USER_MODEL)),
                ('volunteers', models.ManyToManyField(blank=True, null=True, related_name='volunteered_events', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Confirmed', 'Confirmed'), ('Declined', 'Declined'), ('Canceled', 'Canceled')], max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
            ],
            options={
                'unique_together': {('user', 'event')},
            },
        ),
    ]
