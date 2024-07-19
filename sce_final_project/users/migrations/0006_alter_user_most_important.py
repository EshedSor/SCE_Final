# Generated by Django 5.0.2 on 2024-07-19 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_email_alter_user_most_important'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='most_important',
            field=models.CharField(blank=True, choices=[('Organization', 'החמ"ל שלי'), ('Friends', 'להתנדב עם חברים'), ('Distance', 'קרוב לבית'), ('Profession', 'לעסוק במקצוע ובכישורים שלי')], default=None, max_length=30, null=True),
        ),
    ]
