# Generated by Django 5.0.2 on 2024-03-31 10:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ironswords', '0012_alter_user_gender_alter_user_most_important_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='volunteers',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='most_important',
            field=models.CharField(blank=True, choices=[('Distance', 'קרוב לבית'), ('Friends', 'להתנדב עם חברים'), ('Organization', 'החמ"ל שלי'), ('Profession', 'לעסוק במקצוע ובכישורים שלי')], default=None, max_length=30, null=True),
        ),
    ]
