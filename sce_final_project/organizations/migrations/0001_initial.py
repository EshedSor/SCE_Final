# Generated by Django 5.0.2 on 2024-07-19 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, default='')),
                ('contact_name', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('contact_phone', models.CharField(blank=True, default='', max_length=10, null=True)),
            ],
        ),
    ]
