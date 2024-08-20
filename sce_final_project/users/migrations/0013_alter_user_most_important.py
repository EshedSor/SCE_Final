# Generated by Django 5.0.2 on 2024-07-22 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_user_gender_alter_user_most_important'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='most_important',
            field=models.CharField(blank=True, choices=[('Organization', 'החמ"ל שלי'), ('Profession', 'לעסוק במקצוע ובכישורים שלי'), ('Friends', 'להתנדב עם חברים'), ('Distance', 'קרוב לבית')], default=None, max_length=30, null=True),
        ),
    ]
