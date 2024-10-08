# Generated by Django 5.0.2 on 2024-07-22 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_user_most_important'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('F', 'Female'), ('M', 'Male')], default=None, max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='most_important',
            field=models.CharField(blank=True, choices=[('Friends', 'להתנדב עם חברים'), ('Profession', 'לעסוק במקצוע ובכישורים שלי'), ('Distance', 'קרוב לבית'), ('Organization', 'החמ"ל שלי')], default=None, max_length=30, null=True),
        ),
    ]
