# Generated by Django 5.0.2 on 2024-07-21 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_friends_alter_user_most_important'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='most_important',
            field=models.CharField(blank=True, choices=[('Organization', 'החמ"ל שלי'), ('Distance', 'קרוב לבית'), ('Friends', 'להתנדב עם חברים'), ('Profession', 'לעסוק במקצוע ובכישורים שלי')], default=None, max_length=30, null=True),
        ),
    ]
