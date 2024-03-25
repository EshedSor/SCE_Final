# Generated by Django 5.0.2 on 2024-03-25 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ironswords', '0009_alter_user_gender_alter_user_most_important_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Declined', 'Declined'), ('Canceled', 'Canceled')], max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='most_important',
            field=models.CharField(blank=True, choices=[('Profession', 'לעסוק במקצוע ובכישורים שלי'), ('Organization', 'החמ"ל שלי'), ('Friends', 'להתנדב עם חברים'), ('Distance', 'קרוב לבית')], default=None, max_length=30, null=True),
        ),
    ]
